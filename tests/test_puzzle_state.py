"""Tests for the PuzzleState class."""

import numpy as np
from iq_puzzler.puzzle_piece import PuzzlePiece
import json


def test_initialization(mocked_state):
    """Test puzzle mocked_state initialization."""
    assert not mocked_state._placements
    assert not mocked_state._occupied_indices


def test_place_piece_success(mocked_state, mock_piece):
    """Test successful piece placement."""
    # Place piece at origin (index 0)
    assert mocked_state.place_piece(mock_piece, 0)

    # Verify placement
    placement = mocked_state.get_placement(mock_piece.name)
    assert placement is not None
    assert placement.piece.name == mock_piece.name
    assert placement.occupied_indices == {
        0,
        1,
        2,
        5,
    }  # [0,0,0], [1,0,0], [2,0,0], [2,1,0]


def test_place_piece_invalid_position(mocked_state, mock_piece):
    """Test placing piece at invalid position."""
    # Try to place piece at index 6 (far up)
    # This would put parts of the piece outside the valid area
    assert not mocked_state.place_piece(mock_piece, 6)
    assert not mocked_state._placements
    assert not mocked_state._occupied_indices


def test_place_piece_overlap(mocked_state, mock_piece):
    """Test placing pieces with overlap."""
    # Place first piece at origin
    assert mocked_state.place_piece(mock_piece, 0)

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
    assert not mocked_state.place_piece(piece2, 1)  # Would overlap with first piece


def test_place_same_piece_twice(mocked_state, mock_piece):
    """Test placing the same piece twice."""
    assert mocked_state.place_piece(mock_piece, 0)
    assert not mocked_state.place_piece(mock_piece, 1)  # Should fail


def test_remove_piece(mocked_state, mock_piece):
    """Test piece removal."""
    # Place and then remove piece
    mocked_state.place_piece(mock_piece, 0)
    assert mocked_state.remove_piece(mock_piece.name)
    assert not mocked_state._placements
    assert not mocked_state._occupied_indices


def test_remove_nonexistent_piece(mocked_state):
    """Test removing a piece that isn't placed."""
    assert not mocked_state.remove_piece("nonexistent")


def test_get_placement(mocked_state, mock_piece):
    """Test getting placement information."""
    # Test non-existent piece
    assert mocked_state.get_placement(mock_piece.name) is None

    # Place piece and test again
    mocked_state.place_piece(mock_piece, 0)
    placement = mocked_state.get_placement(mock_piece.name)
    assert placement is not None
    assert placement.piece.name == mock_piece.name
    assert placement.occupied_indices == {
        0,
        1,
        2,
        5,
    }  # [0,0,0], [1,0,0], [2,0,0], [2,1,0]


def test_get_occupied_indices(mocked_state, mock_piece):
    """Test getting all occupied indices."""
    assert not mocked_state.get_occupied_indices()

    mocked_state.place_piece(mock_piece, 0)
    assert mocked_state.get_occupied_indices() == {
        0,
        1,
        2,
        5,
    }  # [0,0,0], [1,0,0], [2,0,0], [2,1,0]


def test_get_placements(mocked_state, mock_piece):
    """Test getting all placed pieces."""
    assert not mocked_state.get_placements()

    mocked_state.place_piece(mock_piece, 0)
    placements = mocked_state.get_placements()
    assert len(placements) == 1
    assert placements[0].piece.name == mock_piece.name
    assert placements[0].occupied_indices == {
        0,
        1,
        2,
        5,
    }  # [0,0,0], [1,0,0], [2,0,0], [2,1,0]


def test_export_to_json(mocked_state, mock_piece, tmp_path):
    """Test exporting puzzle state to JSON."""
    # Place a piece
    mocked_state.place_piece(mock_piece, 0)

    # Export to temporary file
    output_file = tmp_path / "test_export.json"
    mocked_state.export_to_json(str(output_file))

    # Read and verify the exported JSON
    with open(output_file) as f:
        data = json.load(f)

    # Verify structure for occupied position
    pos_0 = data["0"]
    assert pos_0["occupied"] is True
    assert pos_0["piece_name"] == mock_piece.name
    assert pos_0["piece_color"] == mock_piece.color
    assert "coordinate" in pos_0
    assert all(isinstance(pos_0["coordinate"][k], float) for k in ["x", "y", "z"])

    # Verify structure for unoccupied position
    pos_3 = data["3"]
    assert pos_3["occupied"] is False
    assert pos_3["piece_name"] is None
    assert pos_3["piece_color"] is None
    assert "coordinate" in pos_3
    assert all(isinstance(pos_3["coordinate"][k], float) for k in ["x", "y", "z"])
