const gridContainer = document.getElementById('grid-container');
const colorNameInput = document.getElementById('color-name-input');
const colorWheel = document.getElementById('color-wheel');
const realColorPicker = document.getElementById('real-color-picker');
const pickColorButton = document.getElementById('pick-color-button');
const savePieceButton = document.getElementById('save-piece-button');
const libraryList = document.getElementById('library-list');
const exportLibraryButton = document.getElementById('export-library-button');
const importLibraryInput = document.getElementById('import-library-input');
const importLibraryButton = document.getElementById('import-library-button');

let currentPiece = {
    name: '',
    color: '',
    shape: [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]
};
let pieceLibrary = [];

// --- Grid Interaction ---
function createGrid() {
    for (let i = 0; i < 16; i++) {
        const cell = document.createElement('div');
        cell.classList.add('grid-cell');
        const row = Math.floor(i / 4);
        const col = i % 4;
        cell.dataset.row = row;
        cell.dataset.col = col;
        cell.addEventListener('click', () => toggleCell(row, col, cell));
        gridContainer.appendChild(cell);
    }
}

function toggleCell(row, col, cellElement) {
    currentPiece.shape[row][col] = 1 - currentPiece.shape[row][col]; // Toggle 0 and 1
    cellElement.classList.toggle('active');
}

// --- Color Picking ---
pickColorButton.addEventListener('click', () => {
    realColorPicker.click();
});

realColorPicker.addEventListener('input', (event) => {
    currentPiece.color = event.target.value;
    colorWheel.style.backgroundColor = event.target.value; // Basic feedback
});

// --- Saving Pieces ---
savePieceButton.addEventListener('click', () => {
    const name = colorNameInput.value.trim();
    if (!name || !currentPiece.color || currentPiece.shape.flat().every(val => val === 0)) {
        alert('Please enter a name, pick a color, and define the piece shape.');
        return;
    }

    const newPiece = {
        name: name,
        color: currentPiece.color,
        shape: currentPiece.shape.map(row => [...row]) // Create a copy
    };
    pieceLibrary.push(newPiece);
    updateLibraryDisplay();
    resetPieceEditor();
});

function resetPieceEditor() {
    colorNameInput.value = '';
    currentPiece.color = '';
    colorWheel.style.backgroundColor = '';
    currentPiece.shape = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ];
    const gridCells = document.querySelectorAll('.grid-cell');
    gridCells.forEach(cell => cell.classList.remove('active'));
}

// --- Library Display and Editing ---
function updateLibraryDisplay() {
    libraryList.innerHTML = '';
    pieceLibrary.forEach((piece, index) => {
        const listItem = document.createElement('div');
        listItem.classList.add('library-item');

        const preview = document.createElement('div');
        preview.classList.add('library-item-preview');
        preview.style.backgroundColor = piece.color;

        const nameSpan = document.createElement('span');
        nameSpan.textContent = piece.name;

        const controls = document.createElement('div');
        controls.classList.add('library-item-controls');

        const editButton = document.createElement('button');
        editButton.textContent = 'Edit';
        editButton.addEventListener('click', () => editPiece(index));

        const deleteButton = document.createElement('button');
        deleteButton.textContent = 'Delete';
        deleteButton.addEventListener('click', () => deletePiece(index));

        controls.appendChild(editButton);
        controls.appendChild(deleteButton);

        listItem.appendChild(preview);
        listItem.appendChild(nameSpan);
        listItem.appendChild(controls);
        libraryList.appendChild(listItem);
    });
}

function editPiece(index) {
    const pieceToEdit = pieceLibrary[index];
    colorNameInput.value = pieceToEdit.name;
    currentPiece.color = pieceToEdit.color;
    colorWheel.style.backgroundColor = pieceToEdit.color;
    currentPiece.shape = pieceToEdit.shape.map(row => [...row]); // Create a copy

    const gridCells = document.querySelectorAll('.grid-cell');
    gridCells.forEach(cell => {
        const row = parseInt(cell.dataset.row);
        const col = parseInt(cell.dataset.col);
        if (currentPiece.shape[row][col] === 1) {
            cell.classList.add('active');
        } else {
            cell.classList.remove('active');
        }
    });

    // Remove the piece from the library temporarily (will be re-saved)
    pieceLibrary.splice(index, 1);
    updateLibraryDisplay();
}

function deletePiece(index) {
    if (confirm('Are you sure you want to delete this piece?')) {
        pieceLibrary.splice(index, 1);
        updateLibraryDisplay();
    }
}

// --- Serialization (JSON) ---
exportLibraryButton.addEventListener('click', () => {
    const jsonString = JSON.stringify(pieceLibrary);
    const blob = new Blob([jsonString], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'piece_library.json';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
});

importLibraryButton.addEventListener('click', () => {
    importLibraryInput.click();
});

importLibraryInput.addEventListener('change', (event) => {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            try {
                pieceLibrary = JSON.parse(e.target.result);
                updateLibraryDisplay();
            } catch (error) {
                alert('Error parsing JSON file.');
            }
        };
        reader.readAsText(file);
    }
});

// --- Initialization ---
createGrid();
updateLibraryDisplay(); // Load any previously stored library (you'd need to implement local storage for persistent storage)