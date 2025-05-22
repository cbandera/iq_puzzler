import { NextRequest, NextResponse } from 'next/server';

// Get the API URL from environment variables or use a default for local development
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8080';

// This is a streaming API endpoint that proxies requests to the Python backend
export async function POST(request: NextRequest) {
  try {
    // Get the request data
    const data = await request.json();
    // Expecting puzzleStateContent, libraryContent, and solutionFile (as a hint)
    const { puzzleStateContent, libraryContent, solutionFile } = data;

    // Validate required parameters
    if (!puzzleStateContent || !libraryContent) { // solutionFile is optional here
      return NextResponse.json(
        { error: 'Missing required parameters: puzzleStateContent or libraryContent' },
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
              puzzleStateContent, // Forward content
              libraryContent,   // Forward content
              solutionFile      // Forward filename hint
            }),
          });

          if (!response.ok) {
            let errorData = { error: 'Error connecting to backend service' };
            try {
                errorData = await response.json();
            } catch (e) {
                // If parsing errorData fails, use the default error
                console.error('Failed to parse error response from backend:', e);
            }
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
            controller.enqueue(`data: ${JSON.stringify({ error: true, message: 'Failed to get reader from backend response' })}\n\n`);
            controller.close();
            return;
          }

          // Pump the data from the Python backend to the client
          while (true) {
            const { done, value } = await reader.read();
            if (done) {
              break;
            }
            // value is Uint8Array, decode it to string
            const chunk = new TextDecoder().decode(value);
            controller.enqueue(chunk); // Forward the raw chunk as it's already SSE formatted
          }
        } catch (error) {
          console.error('Error in stream start:', error);
          let errorMessage = 'Internal server error in stream';
          if (error instanceof Error) {
            errorMessage = error.message;
          }
          controller.enqueue(`data: ${JSON.stringify({ error: true, message: errorMessage })}\n\n`);
        } finally {
          controller.close();
        }
      },
    });

    return new Response(stream, {
      headers: {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
      },
    });
  } catch (error) {
    console.error('Error in POST handler:', error);
    let errorMessage = 'Internal server error';
    if (error instanceof Error) {
        errorMessage = error.message;
    }
    return NextResponse.json({ error: errorMessage }, { status: 500 });
  }
}
