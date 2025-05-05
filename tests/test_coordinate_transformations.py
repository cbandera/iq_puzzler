"""Tests for coordinate transformations."""

from iq_puzzler.puzzle_piece import PuzzlePiece, Location3D
from iq_puzzler import coordinate_transformations
import numpy as np
import pytest

from iq_puzzler.coordinates import XY_DIST, Z_DIST


def test_translate(mock_piece):
    """Test creating a translated PuzzlePiece."""
    translated_piece = coordinate_transformations.translate(
        mock_piece, Location3D(2, 2, 2)
    )
    assert np.array_equal(
        translated_piece.positions,
        [
            Location3D(2, 2, 2),
            Location3D(3, 2, 2),
            Location3D(4, 2, 2),
            Location3D(4, 3, 2),
        ],
    )


@pytest.mark.parametrize(
    "yaw, pitch, roll, expected_positions",
    [
        (0, 0, 0, [(0, 0, 0), (1, 0, 0), (2, 0, 0), (2, 1, 0)]),
        (90, 0, 0, [(0, 0, 0), (0, 1, 0), (0, 2, 0), (-1, 2, 0)]),
        (180, 0, 0, [(0, 0, 0), (-1, 0, 0), (-2, 0, 0), (-2, -1, 0)]),
        (270, 0, 0, [(0, 0, 0), (0, -1, 0), (0, -2, 0), (1, -2, 0)]),
        (0, 0, 180, [(0, 0, 0), (1, 0, 0), (2, 0, 0), (2, -1, 0)]),
        (90, 0, 180, [(0, 0, 0), (0, 1, 0), (0, 2, 0), (1, 2, 0)]),
        (180, 0, 180, [(0, 0, 0), (-1, 0, 0), (-2, 0, 0), (-2, 1, 0)]),
        (270, 0, 180, [(0, 0, 0), (0, -1, 0), (0, -2, 0), (-1, -2, 0)]),
        (
            45,
            45,
            90,
            [
                (0, 0, 0),
                (0.5 * XY_DIST, 0.5 * XY_DIST, -1 * Z_DIST),
                (1.0 * XY_DIST, 1.0 * XY_DIST, -2 * Z_DIST),
                (1.5 * XY_DIST, 1.5 * XY_DIST, -1 * Z_DIST),
            ],
        ),
        (
            45,
            45,
            -90,
            [
                (0, 0, 0),
                (0.5 * XY_DIST, 0.5 * XY_DIST, -1 * Z_DIST),
                (1.0 * XY_DIST, 1.0 * XY_DIST, -2 * Z_DIST),
                (0.5 * XY_DIST, 0.5 * XY_DIST, -3 * Z_DIST),
            ],
        ),
        (
            45,
            -45,
            90,
            [
                (0, 0, 0),
                (0.5 * XY_DIST, 0.5 * XY_DIST, 1 * Z_DIST),
                (1.0 * XY_DIST, 1.0 * XY_DIST, 2 * Z_DIST),
                (0.5 * XY_DIST, 0.5 * XY_DIST, 3 * Z_DIST),
            ],
        ),
        (
            45,
            -45,
            -90,
            [
                (0, 0, 0),
                (0.5 * XY_DIST, 0.5 * XY_DIST, 1 * Z_DIST),
                (1.0 * XY_DIST, 1.0 * XY_DIST, 2 * Z_DIST),
                (1.5 * XY_DIST, 1.5 * XY_DIST, 1 * Z_DIST),
            ],
        ),
        (
            135,
            45,
            90,
            [
                (0, 0, 0),
                (-0.5 * XY_DIST, 0.5 * XY_DIST, -1 * Z_DIST),
                (-1.0 * XY_DIST, 1.0 * XY_DIST, -2 * Z_DIST),
                (-1.5 * XY_DIST, 1.5 * XY_DIST, -1 * Z_DIST),
            ],
        ),
        (
            135,
            45,
            -90,
            [
                (0, 0, 0),
                (-0.5 * XY_DIST, 0.5 * XY_DIST, -1 * Z_DIST),
                (-1.0 * XY_DIST, 1.0 * XY_DIST, -2 * Z_DIST),
                (-0.5 * XY_DIST, 0.5 * XY_DIST, -3 * Z_DIST),
            ],
        ),
        (
            135,
            -45,
            90,
            [
                (0, 0, 0),
                (-0.5 * XY_DIST, 0.5 * XY_DIST, 1 * Z_DIST),
                (-1.0 * XY_DIST, 1.0 * XY_DIST, 2 * Z_DIST),
                (-0.5 * XY_DIST, 0.5 * XY_DIST, 3 * Z_DIST),
            ],
        ),
        (
            135,
            -45,
            -90,
            [
                (0, 0, 0),
                (-0.5 * XY_DIST, 0.5 * XY_DIST, 1 * Z_DIST),
                (-1.0 * XY_DIST, 1.0 * XY_DIST, 2 * Z_DIST),
                (-1.5 * XY_DIST, 1.5 * XY_DIST, 1 * Z_DIST),
            ],
        ),
        (
            225,
            45,
            90,
            [
                (0, 0, 0),
                (-0.5 * XY_DIST, -0.5 * XY_DIST, -1 * Z_DIST),
                (-1.0 * XY_DIST, -1.0 * XY_DIST, -2 * Z_DIST),
                (-1.5 * XY_DIST, -1.5 * XY_DIST, -1 * Z_DIST),
            ],
        ),
        (
            225,
            45,
            -90,
            [
                (0, 0, 0),
                (-0.5 * XY_DIST, -0.5 * XY_DIST, -1 * Z_DIST),
                (-1.0 * XY_DIST, -1.0 * XY_DIST, -2 * Z_DIST),
                (-0.5 * XY_DIST, -0.5 * XY_DIST, -3 * Z_DIST),
            ],
        ),
        (
            225,
            -45,
            90,
            [
                (0, 0, 0),
                (-0.5 * XY_DIST, -0.5 * XY_DIST, 1 * Z_DIST),
                (-1.0 * XY_DIST, -1.0 * XY_DIST, 2 * Z_DIST),
                (-0.5 * XY_DIST, -0.5 * XY_DIST, 3 * Z_DIST),
            ],
        ),
        (
            225,
            -45,
            -90,
            [
                (0, 0, 0),
                (-0.5 * XY_DIST, -0.5 * XY_DIST, 1 * Z_DIST),
                (-1.0 * XY_DIST, -1.0 * XY_DIST, 2 * Z_DIST),
                (-1.5 * XY_DIST, -1.5 * XY_DIST, 1 * Z_DIST),
            ],
        ),
        (
            315,
            45,
            90,
            [
                (0, 0, 0),
                (0.5 * XY_DIST, -0.5 * XY_DIST, -1 * Z_DIST),
                (1.0 * XY_DIST, -1.0 * XY_DIST, -2 * Z_DIST),
                (1.5 * XY_DIST, -1.5 * XY_DIST, -1 * Z_DIST),
            ],
        ),
        (
            315,
            45,
            -90,
            [
                (0, 0, 0),
                (0.5 * XY_DIST, -0.5 * XY_DIST, -1 * Z_DIST),
                (1.0 * XY_DIST, -1.0 * XY_DIST, -2 * Z_DIST),
                (0.5 * XY_DIST, -0.5 * XY_DIST, -3 * Z_DIST),
            ],
        ),
        (
            315,
            -45,
            90,
            [
                (0, 0, 0),
                (0.5 * XY_DIST, -0.5 * XY_DIST, 1 * Z_DIST),
                (1.0 * XY_DIST, -1.0 * XY_DIST, 2 * Z_DIST),
                (0.5 * XY_DIST, -0.5 * XY_DIST, 3 * Z_DIST),
            ],
        ),
        (
            315,
            -45,
            -90,
            [
                (0, 0, 0),
                (0.5 * XY_DIST, -0.5 * XY_DIST, 1 * Z_DIST),
                (1.0 * XY_DIST, -1.0 * XY_DIST, 2 * Z_DIST),
                (1.5 * XY_DIST, -1.5 * XY_DIST, 1 * Z_DIST),
            ],
        ),
    ],
)
def test_rotate(mock_piece, yaw, pitch, roll, expected_positions):
    """Test creating a rotated PuzzlePiece for all valid rotations."""
    rotation_matrix = coordinate_transformations.rotation_matrix(yaw, pitch, roll)
    assert coordinate_transformations.is_rotation_matrix_orthogonal(rotation_matrix)
    rotated_piece = coordinate_transformations.rotate(mock_piece, rotation_matrix)
    assert rotated_piece is not None
    assert isinstance(rotated_piece, PuzzlePiece)
    assert len(rotated_piece.positions) == len(mock_piece.positions)
    assert len(rotated_piece.positions) == len(expected_positions)
    np.testing.assert_allclose(rotated_piece.positions, expected_positions, atol=1e-10)


def test_align_with_grid_positions_invalid():
    """Test that invalid grid positions raise ValueError."""
    invalid_positions = np.array([[0, 0, 0.3], [1, 1, 1]])  # Invalid Z coordinate
    with pytest.raises(ValueError, match="Z direction"):
        coordinate_transformations.align_with_grid_positions(invalid_positions)

    invalid_positions = np.array([[0.3, 0, 0], [1, 1, 0]])  # Invalid X coordinate
    with pytest.raises(ValueError, match="X/Y direction"):
        coordinate_transformations.align_with_grid_positions(invalid_positions)


def test_rotate_invalid():
    """Test that invalid rotations raise ValueError."""
    piece = PuzzlePiece(
        "Test",
        "rgb(255, 0, 0)",
        [Location3D(0, 0, 0), Location3D(1, 0, 0)],
    )
    # Create a rotation matrix that would result in invalid grid positions
    invalid_matrix = np.array(
        [[np.cos(0.1), -np.sin(0.1), 0], [np.sin(0.1), np.cos(0.1), 0], [0, 0, 1]]
    )
    with pytest.raises(ValueError):
        coordinate_transformations.rotate(piece, invalid_matrix)
