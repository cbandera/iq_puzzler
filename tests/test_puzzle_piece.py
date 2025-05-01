from iq_puzzler.puzzle_piece import PuzzlePiece, Location3D
import numpy as np


def test_puzzle_piece_initialization():
    """Test basic initialization of a PuzzlePiece."""
    name = "Test Piece"
    color = "rgb(255, 0, 0)"
    shape = [Location3D(0, 0, 0), Location3D(1, 0, 0), Location3D(0, 1, 0)]

    piece = PuzzlePiece(name, color, shape)

    assert piece.name == name
    assert piece.color == color
    assert np.array_equal(piece.positions, shape)


def test_puzzle_piece_from_json_basic():
    """Test creating a PuzzlePiece from JSON with default scaling."""
    json_data = {
        "name": "Red Piece",
        "color": "rgb(255, 0, 0)",
        "grid": [
            True,
            True,
            False,
            False,
            True,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
        ],
    }

    piece = PuzzlePiece.from_json(json_data)

    assert piece.name == "Red Piece"
    assert piece.color == "rgb(255, 0, 0)"
    expected_positions = [Location3D(0, 0, 0), Location3D(1, 0, 0), Location3D(0, 1, 0)]
    assert np.array_equal(piece.positions, expected_positions)
