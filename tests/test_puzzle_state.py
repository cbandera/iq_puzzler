"""Tests for the PuzzleState class."""

import pytest
import numpy as np
from iq_puzzler.puzzle_state import PuzzleState
from iq_puzzler.puzzle_piece import PuzzlePiece
from iq_puzzler.coordinates import Location3D
from iq_puzzler.puzzle_model import PuzzleModel


class MockPuzzleModel(PuzzleModel):
    """Mock puzzle model for testing."""

    def __init__(self):
        """Initialize with a simple 2x2 grid at z=0."""
        self.valid_coords = {
            tuple(np.array([0.0, 0.0, 0.0])): 0,
            tuple(np.array([1.0, 0.0, 0.0])): 1,
            tuple(np.array([0.0, 1.0, 0.0])): 2,
            tuple(np.array([1.0, 1.0, 0.0])): 3,
        }

    def coord_to_index(self, coord: Location3D) -> int | None:
        """Convert coordinates to index."""
        return self.valid_coords.get(tuple(coord))

    def index_to_coord(self, index: int) -> Location3D | None:
        """Convert index to coordinates."""
        for coord_tuple, idx in self.valid_coords.items():
            if idx == index:
                return np.array(coord_tuple)
        return None

    def is_valid_index(self, index: int) -> bool:
        """Check if index is valid."""
        return index in range(4)

    def is_valid_coord(self, coord: Location3D) -> bool:
        """Check if coordinates are valid."""
        return tuple(coord) in self.valid_coords

    def get_all_indices(self) -> list[int]:
        """Get all valid indices."""
        return list(range(4))


@pytest.fixture
def model():
    """Create a mock puzzle model."""
    return MockPuzzleModel()


@pytest.fixture
def state(model):
    """Create an empty puzzle state."""
    return PuzzleState(model)


@pytest.fixture
def piece():
    """Create a simple L-shaped piece."""
    positions = np.array(
        [
            [0.0, 0.0, 0.0],  # Origin
            [1.0, 0.0, 0.0],  # Right
            [0.0, 1.0, 0.0],  # Up
        ]
    )
    return PuzzlePiece("L", "#FF0000", positions)


def test_initialization(state):
    """Test puzzle state initialization."""
    assert not state._placements
    assert not state._occupied_indices


def test_place_piece_success(state, piece):
    """Test successful piece placement."""
    # Place piece at origin (index 0)
    assert state.place_piece(piece, 0)

    # Verify placement
    placement = state.get_placement(piece.name)
    assert placement is not None
    assert placement.piece.name == piece.name
    assert placement.occupied_indices == {0, 1, 2}


def test_place_piece_invalid_position(state, piece):
    """Test placing piece at invalid position."""
    # Try to place piece at index 3 (top-right)
    # This would put parts of the piece outside the valid area
    assert not state.place_piece(piece, 3)
    assert not state._placements
    assert not state._occupied_indices


def test_place_piece_overlap(state, piece):
    """Test placing pieces with overlap."""
    # Place first piece at origin
    assert state.place_piece(piece, 0)

    # Try to place second piece overlapping first piece
    piece2 = PuzzlePiece(
        "T",
        "#00FF00",
        np.array(
            [
                [1.0, 0.0, 0.0],  # Overlaps with first piece
                [1.0, 1.0, 0.0],
            ]
        ),
    )
    assert not state.place_piece(piece2, 1)  # Would overlap with first piece


def test_place_same_piece_twice(state, piece):
    """Test placing the same piece twice."""
    assert state.place_piece(piece, 0)
    assert not state.place_piece(piece, 1)  # Should fail


def test_remove_piece(state, piece):
    """Test piece removal."""
    # Place and then remove piece
    state.place_piece(piece, 0)
    assert state.remove_piece(piece.name)
    assert not state._placements
    assert not state._occupied_indices


def test_remove_nonexistent_piece(state):
    """Test removing a piece that isn't placed."""
    assert not state.remove_piece("nonexistent")


def test_get_placement(state, piece):
    """Test getting placement information."""
    # Test non-existent piece
    assert state.get_placement(piece.name) is None

    # Place piece and test again
    state.place_piece(piece, 0)
    placement = state.get_placement(piece.name)
    assert placement is not None
    assert placement.piece.name == piece.name
    assert placement.occupied_indices == {0, 1, 2}


def test_get_occupied_indices(state, piece):
    """Test getting all occupied indices."""
    assert not state.get_occupied_indices()

    state.place_piece(piece, 0)
    assert state.get_occupied_indices() == {0, 1, 2}


def test_get_placements(state, piece):
    """Test getting all placed pieces."""
    assert not state.get_placements()

    state.place_piece(piece, 0)
    placements = state.get_placements()
    assert len(placements) == 1
    assert placements[0].piece.name == piece.name
    assert placements[0].occupied_indices == {0, 1, 2}
