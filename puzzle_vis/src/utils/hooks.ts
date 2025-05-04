import { useEffect } from 'react';

export function useInitializePieceLibrary(initializedRef: React.MutableRefObject<boolean>) {
  useEffect(() => {
    const initializePieceLibrary = () => {
      if (initializedRef.current) return;
      initializedRef.current = true;

      // Load default dataset if no local storage data exists
      const savedLibrary = localStorage.getItem('pieceLibrary');
      console.log('Current localStorage data:', savedLibrary);
      if (!savedLibrary) {
        console.log('Loading default dataset...');
        fetch('/data/piece_library.json')
          .then(response => response.json())
          .then(data => {
            console.log('Default dataset loaded:', data);
            localStorage.setItem('pieceLibrary', JSON.stringify(data));
            // Initialize the piece builder after setting default data
            const event = new Event('piece-library-ready');
            window.dispatchEvent(event);
          })
          .catch(error => console.error('Error loading default piece library:', error));
      } else {
        console.log('Using existing data:', JSON.parse(savedLibrary));
        // If we already have data, just initialize
        const event = new Event('piece-library-ready');
        window.dispatchEvent(event);
      }
    };

    initializePieceLibrary();

    return () => {
      initializedRef.current = false;
    };
  }, [initializedRef]);
}
