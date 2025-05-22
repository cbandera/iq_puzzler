"use client";

import { useState, useEffect } from 'react';
import PuzzleViewer, { PuzzleViewerProps } from '@/components/PuzzleViewer';
import { PuzzleState } from '@/types/puzzle';

// Define a default puzzle path or provide a default puzzle structure
const DEFAULT_PUZZLE_PATH = '/data/default_puzzle.json'; // Assumes a default puzzle in public/data

export default function VisualizerPage() {
  const [puzzleProps, setPuzzleProps] = useState<PuzzleViewerProps>({
    puzzleState: null,
    zScale: 1,
  });
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Attempt to load a default puzzle definition
    fetch(DEFAULT_PUZZLE_PATH)
      .then(response => {
        if (!response.ok) {
          throw new Error(`Failed to load default puzzle from ${DEFAULT_PUZZLE_PATH}: ${response.statusText} (${response.status})`);
        }
        return response.json();
      })
      .then((data: PuzzleState) => {
        setPuzzleProps({ puzzleState: data, zScale: 1 });
        setIsLoading(false);
      })
      .catch(err => {
        console.error("Error loading default puzzle:", err);
        setError(err.message);
        // Fallback to null puzzleState if default load fails, allowing the page to still render the viewer
        setPuzzleProps({ puzzleState: null, zScale: 1 });
        setIsLoading(false);
      });
  }, []);

  if (isLoading) {
    return (
      <main className="flex min-h-screen flex-col items-center justify-center p-24">
        <p>Loading Puzzle Visualizer...</p>
      </main>
    );
  }

  return (
    <main className="flex min-h-screen flex-col items-center p-8">
      <h1 className="text-2xl font-semibold mb-6">Puzzle Visualizer</h1>
      {(error && !puzzleProps.puzzleState) && (
        <div className="mb-4 p-4 bg-red-100 text-red-700 border border-red-400 rounded">
          <p><strong>Error:</strong> Could not load the default puzzle. {error}</p>
          <p>Displaying an empty visualizer. You can import a puzzle state manually.</p>
        </div>
      )}
      <div className="w-full max-w-6xl h-[70vh] border rounded-lg overflow-hidden shadow-lg">
        <PuzzleViewer {...puzzleProps} />
      </div>
    </main>
  );
}
