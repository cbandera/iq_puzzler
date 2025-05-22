import { NextRequest, NextResponse } from 'next/server';

// Get the API URL from environment variables or use a default for local development
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8080';

// This is a streaming API endpoint that proxies requests to the Python backend
export async function POST(request: NextRequest) {
  console.log('[NextProxy] Received POST request to /api/solve-puzzle');
  try {
    // Get the request data
    const data = await request.json();
    const { puzzleStateContent, libraryContent, solutionFile } = data;
    console.log(`[NextProxy] Parsed request body. SolutionFile hint: ${solutionFile}`);
    // console.log(`[NextProxy] puzzleStateContent (first 100 chars): ${puzzleStateContent?.substring(0, 100)}`);
    // console.log(`[NextProxy] libraryContent (first 100 chars): ${libraryContent?.substring(0, 100)}`);

    if (!puzzleStateContent || !libraryContent) {
      console.error('[NextProxy] Missing required parameters: puzzleStateContent or libraryContent');
      return NextResponse.json(
        { error: 'Missing required parameters: puzzleStateContent or libraryContent' },
        { status: 400 }
      );
    }

    const targetUrl = `${API_URL}/api/solve-puzzle`;
    console.log(`[NextProxy] Forwarding solve-puzzle request to Python backend at: ${targetUrl}`);

    const stream = new ReadableStream({
      async start(controller) {
        console.log('[NextProxy] Stream started. Making fetch to Python backend.');
        try {
          const requestBody = JSON.stringify({
            puzzleStateContent,
            libraryContent,
            solutionFile
          });
          // console.log(`[NextProxy] Sending body to Python: ${requestBody.substring(0,200)}...`); // Log part of actual body

          const response = await fetch(targetUrl, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: requestBody,
          });

          console.log(`[NextProxy] Received response from Python backend. Status: ${response.status}`);

          if (!response.ok) {
            let errorData = { error: 'Error connecting to backend service', details: '' };
            try {
                const errorText = await response.text();
                console.error(`[NextProxy] Python backend error response text: ${errorText}`);
                errorData = JSON.parse(errorText); // Try to parse if JSON
            } catch (e) {
                console.error('[NextProxy] Failed to parse error response from Python backend:', e);
                errorData.details = `Status: ${response.status}, StatusText: ${response.statusText}. Response body was not valid JSON.`;
            }
            controller.enqueue(`data: ${JSON.stringify({
              error: true,
              message: errorData.error || 'Error connecting to backend service',
              details: errorData.details
            })}\n\n`);
            controller.close();
            return;
          }

          const reader = response.body?.getReader();
          if (!reader) {
            console.error('[NextProxy] Failed to get reader from Python backend response.');
            controller.enqueue(`data: ${JSON.stringify({ error: true, message: 'Failed to get reader from backend response' })}\n\n`);
            controller.close();
            return;
          }

          console.log('[NextProxy] Successfully got reader. Pumping data from Python backend to client...');
          while (true) {
            const { done, value } = await reader.read();
            if (done) {
              console.log('[NextProxy] Python backend stream finished.');
              break;
            }
            const chunk = new TextDecoder().decode(value);
            // console.log(`[NextProxy] Received chunk from Python: ${chunk}`); // Can be very verbose
            controller.enqueue(chunk);
          }
        } catch (error) {
          console.error('[NextProxy] Error in stream start / fetching from Python backend:', error);
          let errorMessage = 'Internal server error in stream';
          if (error instanceof Error) {
            errorMessage = error.message;
          }
          controller.enqueue(`data: ${JSON.stringify({ error: true, message: errorMessage })}\n\n`);
        } finally {
          console.log('[NextProxy] Stream controller closing.');
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
    console.error('[NextProxy] Error in POST handler:', error);
    let errorMessage = 'Internal server error';
    if (error instanceof Error) {
        errorMessage = error.message;
    }
    return NextResponse.json({ error: errorMessage }, { status: 500 });
  }
}
