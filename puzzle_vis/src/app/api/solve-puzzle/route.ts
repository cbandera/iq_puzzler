import { NextRequest, NextResponse } from 'next/server';
import { exec } from 'child_process';
import { promisify } from 'util';
import { join } from 'path';

const execPromise = promisify(exec);

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
    
    // Build the command with the correct paths
    const command = `iq-puzzler --initial ${puzzleStatePath} --library ${libraryPath} --mode pyramid --solver dlx --output ${solutionPath}`;
    
    console.log('Executing command:', command);
    
    // Execute the command with the correct working directory
    const { stdout, stderr } = await execPromise(command, {
      cwd: '/home/claudio/iq_puzzler' // Set the working directory to the main project root
    });
    
    if (stderr) {
      console.error('Solver error:', stderr);
    }
    
    return NextResponse.json({ 
      success: true, 
      output: stdout || stderr,
      solutionFile
    });
  } catch (error) {
    console.error('Error running solver:', error);
    return NextResponse.json(
      { error: 'Error running solver', details: (error as Error).message },
      { status: 500 }
    );
  }
}
