import { NextRequest, NextResponse } from 'next/server';
import { spawn } from 'child_process';
import { join } from 'path';

// This is a streaming API endpoint
export async function POST(request: NextRequest) {
  try {
    const data = await request.json();
    const { puzzleStateFile, libraryFile, solutionFile } = data;
    
    if (!puzzleStateFile || !libraryFile || !solutionFile) {
      return NextResponse.json(
        { error: 'Missing required parameters' },
        { status: 400 }
      );
    }
    
    // Get the paths relative to the iq_puzzler project root
    const puzzleStatePath = join('puzzle_vis', 'public', 'data', puzzleStateFile);
    const libraryPath = join('data', libraryFile); // Using the library in the main project
    const solutionPath = join('puzzle_vis', 'public', 'data', solutionFile);
    
    // Build the command arguments
    const args = [
      '--initial', puzzleStatePath,
      '--library', libraryPath,
      '--mode', 'pyramid',
      '--solver', 'dlx',
      '--output', solutionPath
    ];
    
    console.log('Executing command: iq-puzzler', args.join(' '));
    
    // Create a new ReadableStream to stream the output
    const stream = new ReadableStream({
      async start(controller) {
        let outputBuffer = '';
        let isCompleted = false;
        let hasError = false;
        
        // Spawn the process
        const process = spawn('iq-puzzler', args, {
          cwd: '/home/claudio/iq_puzzler' // Set the working directory to the main project root
        });
        
        // Handle stdout data
        process.stdout.on('data', (data) => {
          const text = data.toString();
          outputBuffer += text;
          controller.enqueue(`data: ${JSON.stringify({ output: text })}\n\n`);
        });
        
        // Handle stderr data
        process.stderr.on('data', (data) => {
          const text = data.toString();
          outputBuffer += text;
          controller.enqueue(`data: ${JSON.stringify({ output: text, error: true })}\n\n`);
        });
        
        // Handle process completion
        process.on('close', (code) => {
          isCompleted = true;
          hasError = code !== 0;
          
          // Send completion event
          controller.enqueue(`data: ${JSON.stringify({ 
            completed: true, 
            success: !hasError,
            solutionFile,
            exitCode: code
          })}\n\n`);
          
          controller.close();
        });
        
        // Handle process errors
        process.on('error', (err) => {
          console.error('Process error:', err);
          hasError = true;
          
          controller.enqueue(`data: ${JSON.stringify({ 
            error: true, 
            message: err.message 
          })}\n\n`);
          
          controller.close();
        });
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
    console.error('Error running solver:', error);
    return NextResponse.json(
      { error: 'Error running solver', details: (error as Error).message },
      { status: 500 }
    );
  }
}
