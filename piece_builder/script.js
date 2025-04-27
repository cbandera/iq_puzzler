// DOM Elements
const gridContainer = document.getElementById('grid-container');
const colorNameInput = document.getElementById('color-name-input');
const colorWheel = document.getElementById('color-wheel');
const savePieceButton = document.getElementById('save-piece-button');
const libraryContainer = document.getElementById('piece-library');
const clearLibraryButton = document.getElementById('clear-library');
const colorValueDisplay = document.getElementById('color-value');

// Track the piece being edited
let editingPieceElement = null;

// Initialize the color picker
const colorPicker = new iro.ColorPicker('#color-wheel', {
    width: 200,
    color: "#0000ff",
    borderWidth: 1,
    borderColor: "#ccc",
    layout: [
        { 
            component: iro.ui.Wheel,
            options: {}
        },
        {
            component: iro.ui.Slider,
            options: {
                sliderType: 'value'
            }
        }
    ]
});

// Update color display when the color picker value changes
colorPicker.on('color:change', function(color) {
    colorValueDisplay.textContent = color.hexString;
    document.querySelectorAll('.grid-cell.active').forEach(cell => {
        cell.style.backgroundColor = color.hexString;
    });
    
    if (editingPieceElement && savePieceButton.textContent === 'Save Piece') {
        // User changed color while editing a piece
        if (confirm('Do you want to create a new piece instead of editing the current one?')) {
            resetEditor();
        } else {
            // Restore the editing state
            const pieceData = JSON.parse(editingPieceElement.dataset.pieceData);
            colorNameInput.value = pieceData.name;
            colorPicker.color.set(pieceData.color);
            savePieceButton.textContent = 'Update Piece';
        }
    }
});

// Handle name input changes
colorNameInput.addEventListener('input', function() {
    if (editingPieceElement && savePieceButton.textContent === 'Save Piece') {
        // User started typing a new name while editing a piece
        if (confirm('Do you want to create a new piece instead of editing the current one?')) {
            resetEditor();
        } else {
            // Restore the editing state
            const pieceData = JSON.parse(editingPieceElement.dataset.pieceData);
            colorNameInput.value = pieceData.name;
            savePieceButton.textContent = 'Update Piece';
        }
    }
});

// Initialize grid
function initializeGrid() {
    for (let i = 0; i < 16; i++) {
        const cell = document.createElement('div');
        cell.className = 'grid-cell';
        cell.addEventListener('click', function() {
            if (editingPieceElement && savePieceButton.textContent === 'Save Piece') {
                // User started modifying grid while editing a piece
                if (confirm('Do you want to create a new piece instead of editing the current one?')) {
                    resetEditor();
                } else {
                    // Restore the editing state
                    const pieceData = JSON.parse(editingPieceElement.dataset.pieceData);
                    colorNameInput.value = pieceData.name;
                    colorPicker.color.set(pieceData.color);
                    document.querySelectorAll('.grid-cell').forEach((cell, index) => {
                        if (pieceData.grid[index]) {
                            cell.classList.add('active');
                            cell.style.backgroundColor = pieceData.color;
                        } else {
                            cell.classList.remove('active');
                            cell.style.backgroundColor = '#f9f9f9';
                        }
                    });
                    savePieceButton.textContent = 'Update Piece';
                    return;
                }
            }
            
            this.classList.toggle('active');
            if (this.classList.contains('active')) {
                this.style.backgroundColor = colorPicker.color.hexString;
            } else {
                this.style.backgroundColor = '#f9f9f9';
            }
        });
        gridContainer.appendChild(cell);
    }
}

// Load saved library from localStorage
function loadLibrary() {
    const savedLibrary = localStorage.getItem('pieceLibrary');
    if (savedLibrary) {
        const libraryControls = libraryContainer.querySelector('.library-controls');
        const pieces = JSON.parse(savedLibrary);
        
        pieces.forEach(piece => {
            const libraryItem = createLibraryItem(piece.name, piece.color, piece.grid);
            libraryContainer.insertBefore(libraryItem, libraryControls.nextSibling);
        });
    }
}

// Save library to localStorage
function saveLibrary() {
    const pieces = Array.from(document.querySelectorAll('.library-item')).map(item => {
        const name = item.querySelector('.library-item-info span').textContent;
        const color = item.querySelector('.library-item-preview').style.backgroundColor;
        const grid = Array.from(item.querySelectorAll('.library-item-cell')).map(cell => 
            cell.classList.contains('active')
        );
        return { name, color, grid };
    });
    localStorage.setItem('pieceLibrary', JSON.stringify(pieces));
}

// Create library item element
function createLibraryItem(name, color, grid) {
    const gridPreview = document.createElement('div');
    gridPreview.className = 'library-item-grid';
    grid.forEach(isActive => {
        const cell = document.createElement('div');
        cell.className = 'library-item-cell';
        if (isActive) {
            cell.classList.add('active');
            cell.style.backgroundColor = color;
        }
        gridPreview.appendChild(cell);
    });

    const libraryItem = document.createElement('div');
    libraryItem.className = 'library-item';
    libraryItem.innerHTML = `
        <div class="library-item-info">
            <span>${name}</span>
            <div class="library-item-preview" style="background-color: ${color}"></div>
        </div>
    `;
    libraryItem.insertBefore(gridPreview, libraryItem.firstChild);
    
    const controls = document.createElement('div');
    controls.className = 'library-item-controls';
    controls.innerHTML = `
        <button class="edit-button" onclick="editPiece(this)">Edit</button>
        <button class="delete-button" onclick="deletePiece(this)">Delete</button>
    `;
    libraryItem.appendChild(controls);
    
    // Store the piece data for easy access
    libraryItem.dataset.pieceData = JSON.stringify({ name, color, grid });
    
    return libraryItem;
}

// Edit piece
function editPiece(button) {
    const libraryItem = button.closest('.library-item');
    const pieceData = JSON.parse(libraryItem.dataset.pieceData);
    
    // Load piece data into editor
    colorNameInput.value = pieceData.name;
    colorPicker.color.set(pieceData.color);
    
    // Update grid
    const gridCells = document.querySelectorAll('.grid-cell');
    gridCells.forEach((cell, index) => {
        if (pieceData.grid[index]) {
            cell.classList.add('active');
            cell.style.backgroundColor = pieceData.color;
        } else {
            cell.classList.remove('active');
            cell.style.backgroundColor = '#f9f9f9';
        }
    });
    
    // Store reference to the piece being edited
    editingPieceElement = libraryItem;
    
    // Change save button text
    savePieceButton.textContent = 'Update Piece';
}

// Delete piece and update storage
function deletePiece(button) {
    const libraryItem = button.closest('.library-item');
    if (editingPieceElement === libraryItem) {
        resetEditor();
    }
    libraryItem.remove();
    saveLibrary();
}

// Reset editor to initial state
function resetEditor() {
    editingPieceElement = null;
    savePieceButton.textContent = 'Save Piece';
    document.querySelectorAll('.grid-cell').forEach(cell => {
        cell.classList.remove('active');
        cell.style.backgroundColor = '#f9f9f9';
    });
    colorNameInput.value = '';
}

// Clear all pieces
clearLibraryButton.addEventListener('click', function() {
    if (confirm('Are you sure you want to clear all pieces? This cannot be undone.')) {
        Array.from(libraryContainer.querySelectorAll('.library-item')).forEach(item => item.remove());
        localStorage.removeItem('pieceLibrary');
        resetEditor();
    }
});

// Save piece functionality
savePieceButton.addEventListener('click', function() {
    const name = colorNameInput.value;
    const color = colorPicker.color.hexString;
    const grid = Array.from(document.querySelectorAll('.grid-cell')).map(cell => 
        cell.classList.contains('active')
    );
    
    const libraryItem = createLibraryItem(name, color, grid);
    const libraryControls = libraryContainer.querySelector('.library-controls');
    
    if (editingPieceElement) {
        // Replace the existing piece
        libraryContainer.replaceChild(libraryItem, editingPieceElement);
    } else {
        // Add new piece
        libraryContainer.insertBefore(libraryItem, libraryControls.nextSibling);
    }
    
    // Save to localStorage
    saveLibrary();
    
    // Reset the editor
    resetEditor();
});

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeGrid();
    loadLibrary();
});