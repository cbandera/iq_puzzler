console.log('piece-builder.js loaded and executing');

let initialized = false;

// Initialize when the piece library is ready
window.addEventListener('piece-library-ready', () => {
  // Always reinitialize when the event is received
  // This ensures the library is loaded when switching between pages
  console.log('Piece library ready event received');
  initialized = true;
  
  // DOM Elements
  const gridContainer = document.getElementById('grid-container');
  const colorNameInput = document.getElementById('color-name-input');
  const colorWheel = document.getElementById('color-wheel');
  const savePieceButton = document.getElementById('save-piece-button');
  const libraryContainer = document.querySelector('.library-items');
  const clearLibraryButton = document.getElementById('clear-library');
  const colorValueDisplay = document.getElementById('color-value');
  const exportLibraryButton = document.getElementById('export-library');
  const importInput = document.getElementById('import-input');
  const importButton = document.getElementById('import-library');
  const resetLibraryButton = document.getElementById('reset-library');

  console.log('DOM elements found:', {
    gridContainer: !!gridContainer,
    colorNameInput: !!colorNameInput,
    colorWheel: !!colorWheel,
    savePieceButton: !!savePieceButton,
    libraryContainer: !!libraryContainer,
    clearLibraryButton: !!clearLibraryButton,
    colorValueDisplay: !!colorValueDisplay,
    exportLibraryButton: !!exportLibraryButton,
    importInput: !!importInput,
    importButton: !!importButton,
    resetLibraryButton: !!resetLibraryButton
  })

  if (!gridContainer || !colorNameInput || !colorWheel || !savePieceButton || 
      !libraryContainer || !clearLibraryButton || !colorValueDisplay || 
      !exportLibraryButton || !importInput || !importButton || !resetLibraryButton) {
    console.error('Required DOM elements not found');
    return;
  }

  // Track the piece being edited
  let editingPieceElement = null;

  // Check if iro is available before initializing the color picker
  if (!window.iro) {
    console.error('iro is not available yet. Cannot initialize color picker.');
    return; // Exit early if iro is not available
  }
  
  // Initialize the color picker
  const colorPicker = new window.iro.ColorPicker('#color-wheel', {
    width: 200,
    color: "#0000ff",
    borderWidth: 1,
    borderColor: "#ccc",
    layout: [
      {
        component: window.iro.ui.Wheel,
        options: {}
      },
      {
        component: window.iro.ui.Slider,
        options: {
          sliderType: 'value'
        }
      }
    ]
  });

  // Update color value display and grid when color changes
  colorPicker.on('color:change', function(color) {
    colorValueDisplay.textContent = color.hexString;
    
    // Update active grid cells with new color
    const cells = gridContainer.children;
    Array.from(cells).forEach(cell => {
      if (cell.dataset.active === 'true') {
        cell.style.backgroundColor = color.hexString;
      }
    });
  });

  // Convert RGB to Hex
  function rgbToHex(rgb) {
    // Check if already hex
    if (rgb.startsWith('#')) return rgb;
    
    // Parse RGB format
    const matches = rgb.match(/^rgb\((\d+),\s*(\d+),\s*(\d+)\)$/);
    if (!matches) return rgb;
    
    const r = parseInt(matches[1]);
    const g = parseInt(matches[2]);
    const b = parseInt(matches[3]);
    
    return '#' + ((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1);
  }

  // Initialize grid with axes visualization
  function initializeGrid() {
    // Clear and set up the grid container
    gridContainer.innerHTML = '';
    gridContainer.style.position = 'relative';
    
    // Create a wrapper for the grid and axes
    const gridWrapper = document.createElement('div');
    gridWrapper.style.position = 'relative';
    gridWrapper.style.width = '140px'; // 4 cells * 30px + 3 gaps * 5px + extra space for axes
    gridWrapper.style.height = '140px'; // 4 cells * 30px + 3 gaps * 5px + extra space for axes
    gridWrapper.style.marginBottom = '20px';
    
    // Create the grid
    const actualGrid = document.createElement('div');
    actualGrid.style.display = 'grid';
    actualGrid.style.gridTemplateColumns = 'repeat(4, 30px)';
    actualGrid.style.gap = '5px';
    actualGrid.style.position = 'absolute';
    actualGrid.style.top = '0';
    actualGrid.style.left = '0';
    
    // Add cells to the grid
    for (let i = 0; i < 16; i++) {
      const cell = document.createElement('div');
      cell.className = 'grid-cell';
      cell.style.width = '30px';
      cell.style.height = '30px';
      cell.style.border = '1px solid #eee';
      cell.style.backgroundColor = '#f9f9f9';
      cell.style.cursor = 'pointer';
      cell.style.borderRadius = '50%';
      cell.dataset.active = 'false';
      
      cell.addEventListener('click', function() {
        this.dataset.active = this.dataset.active === 'true' ? 'false' : 'true';
        this.style.backgroundColor = this.dataset.active === 'true' ? colorPicker.color.hexString : '#f9f9f9';
      });
      
      actualGrid.appendChild(cell);
    }
    
    // Add the grid to the wrapper
    gridWrapper.appendChild(actualGrid);
    
    // Create X axis (upwards, red)
    const xAxis = document.createElement('div');
    xAxis.style.position = 'absolute';
    xAxis.style.bottom = '0';
    xAxis.style.right = '0';
    xAxis.style.width = '2px';
    xAxis.style.height = '80px';
    xAxis.style.backgroundColor = 'red';
    xAxis.style.transform = 'translateX(15px)'; // Center on the last column
    
    // X axis arrow
    const xArrow = document.createElement('div');
    xArrow.style.position = 'absolute';
    xArrow.style.top = '-10px';
    xArrow.style.left = '-4px';
    xArrow.style.width = '0';
    xArrow.style.height = '0';
    xArrow.style.borderLeft = '5px solid transparent';
    xArrow.style.borderRight = '5px solid transparent';
    xArrow.style.borderBottom = '10px solid red';
    
    // X axis label
    const xLabel = document.createElement('div');
    xLabel.style.position = 'absolute';
    xLabel.style.top = '-25px';
    xLabel.style.left = '-5px';
    xLabel.style.color = 'red';
    xLabel.style.fontWeight = 'bold';
    xLabel.textContent = 'X';
    
    xAxis.appendChild(xArrow);
    xAxis.appendChild(xLabel);
    
    // Create Y axis (leftwards, green)
    const yAxis = document.createElement('div');
    yAxis.style.position = 'absolute';
    yAxis.style.bottom = '0';
    yAxis.style.right = '0';
    yAxis.style.height = '2px';
    yAxis.style.width = '80px';
    yAxis.style.backgroundColor = 'green';
    yAxis.style.transform = 'translateY(15px)'; // Center on the bottom row
    
    // Y axis arrow
    const yArrow = document.createElement('div');
    yArrow.style.position = 'absolute';
    yArrow.style.left = '-10px';
    yArrow.style.top = '-4px';
    yArrow.style.width = '0';
    yArrow.style.height = '0';
    yArrow.style.borderTop = '5px solid transparent';
    yArrow.style.borderBottom = '5px solid transparent';
    yArrow.style.borderRight = '10px solid green';
    
    // Y axis label
    const yLabel = document.createElement('div');
    yLabel.style.position = 'absolute';
    yLabel.style.left = '-25px';
    yLabel.style.top = '-8px';
    yLabel.style.color = 'green';
    yLabel.style.fontWeight = 'bold';
    yLabel.textContent = 'Y';
    
    yAxis.appendChild(yArrow);
    yAxis.appendChild(yLabel);
    
    // Add axes to the wrapper
    gridWrapper.appendChild(xAxis);
    gridWrapper.appendChild(yAxis);
    
    // Add the wrapper to the grid container
    gridContainer.appendChild(gridWrapper);
    
    // Add a small legend explaining the coordinate system
    const legend = document.createElement('div');
    legend.style.marginTop = '10px';
    legend.style.fontSize = '12px';
    legend.style.color = '#666';
    legend.innerHTML = 'Coordinate system: <span style="color:red;font-weight:bold">X</span> (up), <span style="color:green;font-weight:bold">Y</span> (left) starting from bottom right';
    
    gridContainer.appendChild(legend);
  }

  // Load saved library from localStorage
  function loadLibrary(pieces) {
    console.log('Loading library from data:', pieces);
    try {
      libraryContainer.innerHTML = ''; // Clear existing items
      
      // Sort pieces by name
      const sortedPieces = pieces.sort((a, b) => a.name.localeCompare(b.name));
      
      sortedPieces.forEach(piece => {
        console.log('Creating library item:', piece);
        createLibraryItem(piece.name, piece.color, piece.grid);
      });
      updatePieceCount();
    } catch (error) {
      console.error('Error loading library:', error);
    }
  }

  // Save library to localStorage
  function saveLibrary() {
    const pieces = Array.from(libraryContainer.querySelectorAll('.library-item')).map(item => ({
      name: item.querySelector('.library-item-name').textContent,
      color: item.querySelector('.library-item-grid').dataset.color,
      grid: JSON.parse(item.querySelector('.library-item-grid').dataset.grid)
    }));
    localStorage.setItem('pieceLibrary', JSON.stringify(pieces));
    updatePieceCount();
  }

  // Create library item element
  function createLibraryItem(name, color, grid) {
    const hexColor = rgbToHex(color);
    console.log('Converting color:', color, 'to hex:', hexColor);
    
    const item = document.createElement('div');
    item.className = 'library-item flex items-center justify-between p-3 mb-3 border rounded bg-white hover:shadow-sm w-full';
    
    const leftContent = document.createElement('div');
    leftContent.className = 'flex items-center gap-4 flex-1';
    
    const gridElement = document.createElement('div');
    gridElement.className = 'library-item-grid';  
    gridElement.style.display = 'grid';
    gridElement.style.gridTemplateColumns = 'repeat(4, 15px)';
    gridElement.style.gap = '1px';
    gridElement.dataset.color = hexColor;
    gridElement.dataset.grid = JSON.stringify(grid);
    
    const nameElement = document.createElement('span');
    nameElement.className = 'library-item-name font-medium';  
    nameElement.textContent = name;
    
    // Build the layout: grid -> name -> buttons
    leftContent.appendChild(gridElement);
    leftContent.appendChild(nameElement);
    
    const buttonsContainer = document.createElement('div');
    buttonsContainer.className = 'flex gap-2 ml-auto';  
    
    const editButton = document.createElement('button');
    editButton.className = 'px-2 py-1 text-sm bg-blue-500 text-white rounded hover:bg-blue-600';
    editButton.textContent = 'Edit';
    editButton.onclick = () => editPiece(editButton);
    
    const deleteButton = document.createElement('button');
    deleteButton.className = 'px-2 py-1 text-sm bg-red-500 text-white rounded hover:bg-red-600';
    deleteButton.textContent = 'Delete';
    deleteButton.onclick = () => deletePiece(deleteButton);
    
    buttonsContainer.appendChild(editButton);
    buttonsContainer.appendChild(deleteButton);
    
    item.appendChild(leftContent);
    item.appendChild(buttonsContainer);
    
    const grid4x4 = grid.slice(0, 16);
    grid4x4.forEach(cell => {
      const cellElement = document.createElement('div');
      cellElement.style.width = '15px';
      cellElement.style.height = '15px';
      cellElement.style.backgroundColor = cell ? hexColor : 'transparent';
      cellElement.style.border = '1px solid #eee';
      cellElement.style.borderRadius = '50%';
      gridElement.appendChild(cellElement);
    });
    
    // Find the correct position to insert the item (sorted by name)
    const items = Array.from(libraryContainer.children);
    const insertIndex = items.findIndex(existing => {
      const existingName = existing.querySelector('.library-item-name').textContent;
      return existingName.localeCompare(name) > 0;
    });
    
    if (insertIndex === -1) {
      libraryContainer.appendChild(item);
    } else {
      libraryContainer.insertBefore(item, items[insertIndex]);
    }
  }

  // Edit an existing piece
  function editPiece(button) {
    const item = button.closest('.library-item');
    const name = item.querySelector('.library-item-name').textContent;
    const gridElement = item.querySelector('.library-item-grid');
    const color = gridElement.dataset.color;
    const grid = JSON.parse(gridElement.dataset.grid);
    
    // Set the editing state
    editingPieceElement = item;
    savePieceButton.textContent = 'Update';
    
    // Set the color name input
    colorNameInput.value = name;

    // Convert color to hex if needed
    const hexColor = rgbToHex(color);
    console.log('Setting color picker to:', hexColor);
    colorPicker.color.hexString = hexColor;
  
    // Reset all grid cells first
    const gridWrapper = gridContainer.querySelector('div'); // Get the wrapper div
    if (!gridWrapper) {
      console.error('Grid wrapper not found');
      return;
    }
    
    const actualGrid = gridWrapper.querySelector('div'); // Get the actual grid div
    if (!actualGrid) {
      console.error('Actual grid not found');
      return;
    }
    
    const cells = actualGrid.querySelectorAll('.grid-cell');
    console.log('Found', cells.length, 'grid cells');
    
    // Reset all cells first
    cells.forEach(cell => {
      cell.dataset.active = 'false';
      cell.style.backgroundColor = '#f9f9f9';
    });
    
    // Apply the piece grid
    const grid4x4 = grid.slice(0, 16);
    grid4x4.forEach((isActive, index) => {
      if (index < cells.length) {
        cells[index].dataset.active = isActive.toString();
        cells[index].style.backgroundColor = isActive ? hexColor : '#f9f9f9';
      }
    });
  }

  // Delete piece and update storage
  function deletePiece(button) {
    if (confirm('Are you sure you want to delete this piece?')) {
      const item = button.closest('.library-item');
      item.remove();
      saveLibrary();
    }
  }

  // Reset editor to initial state
  function resetEditor() {
    editingPieceElement = null;
    savePieceButton.textContent = 'Save';
    colorNameInput.value = '';
    
    // Reset grid cells in the new structure
    const gridWrapper = gridContainer.querySelector('div');
    if (!gridWrapper) {
      console.error('Grid wrapper not found');
      return;
    }
    
    const actualGrid = gridWrapper.querySelector('div');
    if (!actualGrid) {
      console.error('Actual grid not found');
      return;
    }
    
    const cells = actualGrid.querySelectorAll('.grid-cell');
    cells.forEach(cell => {
      cell.dataset.active = 'false';
      cell.style.backgroundColor = '#f9f9f9';
    });
  }

  // Update piece count in the library header
  function updatePieceCount() {
    const count = libraryContainer.querySelectorAll('.library-item').length;
    const countElement = document.getElementById('piece-count');
    if (countElement) {
      countElement.textContent = `(${count} pieces)`;
    }
  }

  // Reset library to default
  async function resetLibrary() {
    if (confirm('Are you sure you want to reset to the default library? This will replace all current pieces.')) {
      try {
        console.log('Fetching default piece library...');
        const response = await fetch('/data/piece_library.json');
        if (!response.ok) {
          throw new Error(`Failed to fetch: ${response.status} ${response.statusText}`);
        }
        const defaultPieces = await response.json();
        console.log('Default pieces loaded:', defaultPieces);
        localStorage.setItem('pieceLibrary', JSON.stringify(defaultPieces));
        
        // Make sure the library container is available before loading
        const libraryContainer = document.querySelector('.library-items');
        if (!libraryContainer) {
          console.error('Library container not found');
          alert('Error: Library container not found');
          return;
        }
        
        loadLibrary(defaultPieces);
        console.log('Default library loaded successfully');
      } catch (error) {
        console.error('Error loading default library:', error);
        alert('Error loading default library: ' + error.message);
      }
    }
  }

  // Event listeners
  savePieceButton.addEventListener('click', function() {
    const name = colorNameInput.value.trim();
    if (!name) {
      alert('Please enter a piece name');
      return;
    }
    
    const color = colorPicker.color.hexString;
    
    // Get grid cells from the new structure
    const gridWrapper = gridContainer.querySelector('div'); // Get the wrapper div
    if (!gridWrapper) {
      console.error('Grid wrapper not found');
      return;
    }
    
    const actualGrid = gridWrapper.querySelector('div'); // Get the actual grid div
    if (!actualGrid) {
      console.error('Actual grid not found');
      return;
    }
    
    const cells = actualGrid.querySelectorAll('.grid-cell');
    const grid = Array.from(cells).map(cell => cell.dataset.active === 'true');
    
    if (!grid.some(cell => cell)) {
      alert('Please select at least one cell in the grid');
      return;
    }
    
    if (editingPieceElement) {
      editingPieceElement.remove();
    }
    
    createLibraryItem(name, color, grid);
    saveLibrary();
    resetEditor();
  });

  clearLibraryButton.addEventListener('click', function() {
    if (confirm('Are you sure you want to clear the entire library?')) {
      libraryContainer.innerHTML = '';
      saveLibrary();
    }
  });

  exportLibraryButton.addEventListener('click', function() {
    const pieces = Array.from(libraryContainer.querySelectorAll('.library-item')).map(item => ({
      name: item.querySelector('.library-item-name').textContent,
      color: item.querySelector('.library-item-grid').dataset.color,
      grid: JSON.parse(item.querySelector('.library-item-grid').dataset.grid)
    }));
    
    const blob = new Blob([JSON.stringify(pieces, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'piece-library.json';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  });

  // Import functionality
  importButton.addEventListener('click', function() {
    importInput.click();
  });

  importInput.addEventListener('change', function(e) {
    const file = e.target.files?.[0];
    if (!file) return;
    
    const reader = new FileReader();
    reader.onload = function(e) {
      try {
        const result = e.target?.result;
        if (typeof result !== 'string') {
          throw new Error('Invalid file content');
        }
        
        const pieces = JSON.parse(result);
        if (!Array.isArray(pieces)) {
          throw new Error('Invalid file format: expected an array');
        }
        
        libraryContainer.innerHTML = '';
        pieces.forEach(piece => {
          if (!piece.name || !piece.color || !piece.grid) {
            console.warn('Skipping invalid piece:', piece);
            return;
          }
          createLibraryItem(piece.name, piece.color, piece.grid);
        });
        saveLibrary();
      } catch (error) {
        console.error('Error importing library:', error);
        alert('Error importing library: ' + error.message);
      }
    };
    
    reader.onerror = function() {
      console.error('Error reading file:', reader.error);
      alert('Error reading file');
    };
    
    reader.readAsText(file);
    this.value = ''; // Reset file input
  });

  resetLibraryButton.addEventListener('click', resetLibrary);

  // Load saved library from localStorage or default
  // This is crucial for when switching between pages
  function loadSavedLibrary() {
    console.log('Loading saved library from localStorage');
    const savedLibrary = localStorage.getItem('pieceLibrary');
    if (savedLibrary) {
      try {
        const pieces = JSON.parse(savedLibrary);
        console.log('Found saved pieces:', pieces.length);
        loadLibrary(pieces);
      } catch (error) {
        console.error('Error parsing saved library:', error);
      }
    } else {
      console.log('No saved library found, trying to load default');
      // If no saved library, try to load the default
      fetch('/data/piece_library.json')
        .then(response => {
          if (!response.ok) {
            throw new Error(`Failed to fetch: ${response.status} ${response.statusText}`);
          }
          return response.json();
        })
        .then(defaultPieces => {
          console.log('Default pieces loaded:', defaultPieces);
          localStorage.setItem('pieceLibrary', JSON.stringify(defaultPieces));
          loadLibrary(defaultPieces);
        })
        .catch(error => {
          console.error('Error loading default library:', error);
        });
    }
  }
  
  // Always load the library when initializing
  loadSavedLibrary();

  // Initialize the application
  initializeGrid();
});
