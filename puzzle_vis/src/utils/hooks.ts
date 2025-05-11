import { useEffect } from 'react';

export function useInitializePieceLibrary(initializedRef: React.MutableRefObject<boolean>) {
  useEffect(() => {
    const initializePieceLibrary = () => {
      if (initializedRef.current) return;
      initializedRef.current = true;

      // Load default dataset if no local storage data exists
      const savedLibrary = localStorage.getItem('pieceLibrary');
      console.log('Current localStorage data:', savedLibrary);
      
      // Function to safely dispatch the event only when iro is available
      const safelyDispatchEvent = () => {
        // Check if iro is available in window
        if (typeof window.iro === 'undefined') {
          console.log('iro not available yet, waiting...');
          // Wait and try again
          setTimeout(safelyDispatchEvent, 500);
          return;
        }
        
        console.log('iro is available, dispatching event');
        const event = new Event('piece-library-ready');
        window.dispatchEvent(event);
      };
      
      if (!savedLibrary) {
        console.log('Loading default dataset...');
        fetch('/data/piece_library.json')
          .then(response => response.json())
          .then(data => {
            console.log('Default dataset loaded:', data);
            localStorage.setItem('pieceLibrary', JSON.stringify(data));
            // Initialize the piece builder after setting default data
            safelyDispatchEvent();
          })
          .catch(error => console.error('Error loading default piece library:', error));
      } else {
        console.log('Using existing data:', JSON.parse(savedLibrary));
        // If we already have data, just initialize
        safelyDispatchEvent();
      }
    };

    // Delay initialization slightly to ensure scripts have time to load
    setTimeout(initializePieceLibrary, 100);

    return () => {
      initializedRef.current = false;
    };
  }, [initializedRef]);
}
