from iq_puzzler.puzzle_piece import PuzzlePiece, Location3D
from iq_puzzler.puzzle_piece_transformer import PuzzlePieceTransformer
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
    # With default scaling (2.0), coordinates should be multiplied by 2
    expected_positions = [Location3D(0, 0, 0), Location3D(2, 0, 0), Location3D(0, 2, 0)]
    assert np.array_equal(piece.positions, expected_positions)


def test_puzzle_piece_from_json_custom_scale():
    """Test creating a PuzzlePiece from JSON with custom scaling."""
    json_data = {
        "name": "Blue Piece",
        "color": "rgb(0, 0, 255)",
        "grid": [
            True,
            False,
            False,
            False,
            True,
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
        ],
    }

    piece = PuzzlePiece.from_json(json_data, scale=3.0)

    # With scaling of 3.0, coordinates should be multiplied by 3
    expected_positions = [Location3D(0, 0, 0), Location3D(0, 3, 0), Location3D(3, 3, 0)]
    assert np.array_equal(piece.positions, expected_positions)


def test_puzzle_piece_translated():
    """Test creating a translated PuzzlePiece."""
    transformer = PuzzlePieceTransformer()
    piece = PuzzlePiece(
        "Test", "rgb(255, 0, 0)", [Location3D(0, 0, 0), Location3D(1, 0, 0)]
    )
    translated_piece = transformer.translate(piece, Location3D(2, 2, 2))
    assert np.array_equal(
        translated_piece.positions, [Location3D(2, 2, 2), Location3D(3, 2, 2)]
    )


def test_puzzle_piece_rotated():
    """Test creating a rotated PuzzlePiece."""
    transformer = PuzzlePieceTransformer()
    piece = PuzzlePiece(
        "Test", "rgb(255, 0, 0)", [Location3D(0, 0, 0), Location3D(1, 0, 0)]
    )
    rotation_matrix = np.array([[0, 1, 0], [1, 0, 0], [0, 0, 1]])
    rotated_piece = transformer.rotate(piece, rotation_matrix)
    assert np.array_equal(
        rotated_piece.positions, [Location3D(0, 0, 0), Location3D(0, 1, 0)]
    )
