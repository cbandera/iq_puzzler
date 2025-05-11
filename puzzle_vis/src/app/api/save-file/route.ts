import { NextRequest, NextResponse } from 'next/server';
import { writeFile, mkdir } from 'fs/promises';
import { join } from 'path';
import { existsSync } from 'fs';

export async function POST(request: NextRequest) {
  try {
    const formData = await request.formData();
    const file = formData.get('file') as File;
    const pathParam = formData.get('path') as string;
    
    if (!file) {
      return NextResponse.json(
        { error: 'No file provided' },
        { status: 400 }
      );
    }
    
    // Determine the directory path
    const directoryPath = join(process.cwd(), 'public', pathParam || '');
    
    // Create directory if it doesn't exist
    if (!existsSync(directoryPath)) {
      await mkdir(directoryPath, { recursive: true });
    }
    
    // Create the file path
    const filePath = join(directoryPath, file.name);
    
    // Convert file to buffer
    const buffer = Buffer.from(await file.arrayBuffer());
    
    // Write the file
    await writeFile(filePath, buffer);
    
    return NextResponse.json({ 
      success: true, 
      message: 'File saved successfully',
      path: `/${pathParam}/${file.name}`
    });
  } catch (error) {
    console.error('Error saving file:', error);
    return NextResponse.json(
      { error: 'Error saving file', details: (error as Error).message },
      { status: 500 }
    );
  }
}
