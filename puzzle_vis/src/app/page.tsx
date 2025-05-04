'use client';

import { useState, useEffect } from 'react';
import PuzzleViewer from '@/components/PuzzleViewer';
import { PuzzleState } from '@/types/puzzle';

const DEFAULT_SPHERE_RADIUS = 0.5;
const DEFAULT_Z_SCALE = 1;

export default function Home() {
  const [puzzleState, setPuzzleState] = useState<PuzzleState | null>(null);
  const [sphereRadius, setSphereRadius] = useState(DEFAULT_SPHERE_RADIUS);
  const [zScale, setZScale] = useState(DEFAULT_Z_SCALE);

  useEffect(() => {
    // Load saved state from localStorage on initial render
    const savedState = localStorage.getItem('puzzleState');
    if (savedState) {
      setPuzzleState(JSON.parse(savedState));
    }

    // Load saved sphere radius
    const savedRadius = localStorage.getItem('sphereRadius');
    if (savedRadius) {
      setSphereRadius(parseFloat(savedRadius));
    }

    // Load saved z-scale
    const savedZScale = localStorage.getItem('zScale');
    if (savedZScale) {
      setZScale(parseFloat(savedZScale));
    }
  }, []);

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (e) => {
      try {
        const content = e.target?.result as string;
        const data = JSON.parse(content);
        setPuzzleState(data);
        localStorage.setItem('puzzleState', content);
      } catch (error) {
        console.error('Error parsing JSON file:', error);
        alert('Error parsing JSON file. Please make sure it\'s a valid JSON file.');
      }
    };
    reader.readAsText(file);
  };

  const handleClearPuzzle = () => {
    setPuzzleState(null);
    localStorage.removeItem('puzzleState');
  };

  const handleRadiusChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const newRadius = parseFloat(event.target.value);
    setSphereRadius(newRadius);
    localStorage.setItem('sphereRadius', newRadius.toString());
  };

  const handleZScaleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const newZScale = parseFloat(event.target.value);
    setZScale(newZScale);
    localStorage.setItem('zScale', newZScale.toString());
  };

  const resetSphereRadius = () => {
    setSphereRadius(DEFAULT_SPHERE_RADIUS);
    localStorage.setItem('sphereRadius', DEFAULT_SPHERE_RADIUS.toString());
  };

  const resetZScale = () => {
    setZScale(DEFAULT_Z_SCALE);
    localStorage.setItem('zScale', DEFAULT_Z_SCALE.toString());
  };

  return (
    <main className="min-h-screen p-8">
      <div className="max-w-6xl mx-auto space-y-8">
        <h1 className="text-3xl font-bold">IQ Puzzler Visualizer</h1>
        
        <div className="space-y-4">
          <div className="flex items-center space-x-4">
            <label htmlFor="file-upload" className="block text-sm font-medium mb-2">
              Upload Solution JSON File
            </label>
            <input
              id="file-upload"
              type="file"
              accept=".json"
              onChange={handleFileUpload}
              className="block w-full text-sm border border-gray-300 rounded-lg cursor-pointer bg-gray-50 focus:outline-none"
            />
            <button
              onClick={handleClearPuzzle}
              className="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600"
            >
              Clear Puzzle
            </button>
          </div>

          <div>
            <div className="flex items-center justify-between mb-2">
              <label htmlFor="radius-slider" className="block text-sm font-medium">
                Sphere Radius: {sphereRadius}
              </label>
              <button
                onClick={resetSphereRadius}
                className="px-2 py-1 text-xs bg-gray-100 hover:bg-gray-200 text-gray-600 rounded"
              >
                Reset
              </button>
            </div>
            <input
              id="radius-slider"
              type="range"
              min="0.1"
              max="1"
              step="0.1"
              value={sphereRadius}
              onChange={handleRadiusChange}
              className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
            />
          </div>

          <div>
            <div className="flex items-center justify-between mb-2">
              <label htmlFor="z-scale-slider" className="block text-sm font-medium">
                Z-Axis Scale: {zScale}
              </label>
              <button
                onClick={resetZScale}
                className="px-2 py-1 text-xs bg-gray-100 hover:bg-gray-200 text-gray-600 rounded"
              >
                Reset
              </button>
            </div>
            <input
              id="z-scale-slider"
              type="range"
              min="1"
              max="5"
              step="0.1"
              value={zScale}
              onChange={handleZScaleChange}
              className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
            />
          </div>
        </div>

        {puzzleState && (
          <PuzzleViewer
            puzzleState={puzzleState}
            sphereRadius={sphereRadius}
            zScale={zScale}
          />
        )}
      </div>
    </main>
  );
}
