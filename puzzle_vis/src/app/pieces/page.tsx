'use client'
import { useEffect, useRef } from 'react'
import Script from 'next/script'
import { useInitializePieceLibrary } from '@/utils/hooks';

// Extend Window interface to include iro
declare global {
  interface Window {
    iro?: any;
  }
}

export default function PieceLibrary() {
  const initialized = useRef(false);
  const iroLoaded = useRef(false);

  useInitializePieceLibrary(initialized);

  // Function to initialize the piece builder when both scripts are ready
  const initializePieceBuilder = () => {
    if (iroLoaded.current) {
      console.log('Initializing piece library...');
      const event = new Event('piece-library-ready');
      window.dispatchEvent(event);
    }
  };

  return (
    <div className="flex max-w-[1200px] mx-auto gap-8 p-5">
      <div id="piece-editor" className="flex-1 p-6 border border-gray-300 rounded-lg bg-white">
        <h2 className="text-xl font-semibold mb-4">Piece Editor</h2>
        <div id="grid-container" className="mb-4"></div>
        <div id="color-picker-container" className="mb-5">
          <div className="flex flex-col items-center gap-4 p-4">
            <div className="w-full">
              <label htmlFor="color-name-input" className="block mb-1">Piece Name:</label>
              <input 
                type="text" 
                id="color-name-input"
                className="w-full px-3 py-2 border rounded"
              />
            </div>
            <div id="color-wheel" className="mx-auto"></div>
            <div id="selected-color" className="text-sm">
              Selected Color: <span id="color-value" className="font-mono">#0000ff</span>
            </div>
          </div>
        </div>
        <button
          id="save-piece-button"
          className="w-full bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
        >
          Save Piece
        </button>
      </div>

      <div id="piece-library" className="w-[500px] p-6 border border-gray-300 rounded-lg bg-white">
        <div className="library-header mb-4">
          <div className="flex items-center justify-between mb-2">
            <h2 className="text-xl font-semibold">
              Piece Library <span id="piece-count" className="text-sm text-gray-600">(0 pieces)</span>
            </h2>
            <div className="flex gap-2">
              <input
                type="file"
                id="import-input"
                accept=".json"
                className="hidden"
              />
              <button
                id="import-library"
                onClick={() => document.getElementById('import-input')?.click()}
                className="px-3 py-1 text-sm bg-blue-500 text-white rounded hover:bg-blue-600"
              >
                Import
              </button>
              <button
                id="export-library"
                className="px-3 py-1 text-sm bg-green-500 text-white rounded hover:bg-green-600"
              >
                Export
              </button>
            </div>
          </div>
          <div className="library-controls flex gap-2">
            <button
              id="clear-library"
              className="px-3 py-1 text-sm bg-red-500 text-white rounded hover:bg-red-600"
            >
              Clear All
            </button>
            <button
              id="reset-library"
              className="px-3 py-1 text-sm bg-gray-500 text-white rounded hover:bg-gray-600"
            >
              Reset to Default
            </button>
          </div>
        </div>
        <div className="library-items border rounded-lg p-4 min-h-[700px] bg-gray-50 w-full"></div>
      </div>

      {/* Load iro.js first and ensure it's fully loaded before proceeding */}
      <Script 
        src="https://cdn.jsdelivr.net/npm/@jaames/iro@5"
        strategy="beforeInteractive"
        onLoad={() => {
          console.log('iro.js loaded');
          if (window.iro) {
            console.log('iro is available in window');
            iroLoaded.current = true;
            // Wait for a moment to ensure iro is fully initialized
            setTimeout(() => {
              initializePieceBuilder();
            }, 200);
          } else {
            console.error('iro failed to load properly');
          }
        }}
      />
      
      {/* Load piece-builder.js after iro.js */}
      <Script 
        src="/piece-builder.js"
        strategy="afterInteractive"
        onLoad={() => {
          console.log('piece-builder.js loaded');
        }}
      />
    </div>
  )
}
