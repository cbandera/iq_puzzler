import { NextRequest, NextResponse } from 'next/server';

// Get the API URL from environment variables or use a default for local development
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8080';

// This is a streaming API endpoint that proxies requests to the Python backend
export async function POST(request: NextRequest) {
  try {
    // Get the request data
    const data = await request.json();
    const { puzzleStateFile, libraryFile, solutionFile } = data;

    // Validate required parameters
    if (!puzzleStateFile || !libraryFile || !solutionFile) {
      return NextResponse.json(
        { error: 'Missing required parameters' },
        { status: 400 }
      );
    }

    console.log(`Forwarding solve-puzzle request to Python backend at ${API_URL}`);

    // Create a new ReadableStream to stream the output from the Python backend
    const stream = new ReadableStream({
      async start(controller) {
        try {
          // Forward the request to the Python backend
          const response = await fetch(`${API_URL}/api/solve-puzzle`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              puzzleStateFile,
              libraryFile,
              solutionFile
            }),
          });

          if (!response.ok) {
            const errorData = await response.json();
            controller.enqueue(`data: ${JSON.stringify({
              error: true,
              message: errorData.error || 'Error connecting to backend service'
            })}\n\n`);
            controller.close();
            return;
          }

          // Get the reader from the response body
          const reader = response.body?.getReader();
          if (!reader) {
            throw new Error('Failed to get reader from response');
          }

          // Read and forward the streaming data
          while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            
            // Convert the Uint8Array to a string and forward it
            const text = new TextDecoder().decode(value);
            controller.enqueue(text);
          }
          
          controller.close();
        } catch (error) {
          console.error('Error streaming from Python backend:', error);
          controller.enqueue(`data: ${JSON.stringify({
            error: true,
            message: (error as Error).message
          })}\n\n`);
          controller.close();
        }
      }
    });

    // Return the stream as a Server-Sent Events response
    return new Response(stream, {
      headers: {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive'
      }
    });
  } catch (error) {
    console.error('Error in API route:', error);
    return NextResponse.json(
      { error: 'Error in API route', details: (error as Error).message },
      { status: 500 }
    );
  }
}
