from iq_puzzler.puzzle_piece import PuzzlePiece, Location3D
from iq_puzzler import coordinate_transformations
import numpy as np
import pytest

Z_DIST = coordinate_transformations.Z_DIST
XY_DIST = coordinate_transformations.XY_DIST


def test_rotation_matrix_orthogonality():
    """Test that generated rotation matrices are proper orthogonal matrices."""
    for rotation in coordinate_transformations._ROTATION_MATRICES:
        # Test orthogonality: R.T @ R = I
        identity = rotation.T @ rotation
        np.testing.assert_allclose(identity, np.eye(3), atol=1e-10)

        # Test proper rotation: det(R) = 1
        np.testing.assert_allclose(np.linalg.det(rotation), 1, atol=1e-10)


@pytest.fixture
def example_piece():
    return PuzzlePiece(
        "Test",
        "rgb(255, 0, 0)",
        [
            Location3D(0, 0, 0),
            Location3D(1, 0, 0),
            Location3D(2, 0, 0),
            Location3D(2, 1, 0),
        ],
    )


def test_translate(example_piece):
    """Test creating a translated PuzzlePiece."""
    translated_piece = coordinate_transformations.translate(
        example_piece, Location3D(2, 2, 2)
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
def test_rotate(example_piece, yaw, pitch, roll, expected_positions):
    """Test creating a rotated PuzzlePiece for all valid rotations."""
    assert (yaw, pitch, roll) in coordinate_transformations._VALID_ROTATIONS
    rotation_matrix = coordinate_transformations.rotation_matrix(yaw, pitch, roll)
    rotated_piece = coordinate_transformations.rotate(example_piece, rotation_matrix)
    assert rotated_piece is not None
    assert isinstance(rotated_piece, PuzzlePiece)
    assert len(rotated_piece.positions) == len(example_piece.positions)
    np.testing.assert_allclose(rotated_piece.positions, expected_positions, atol=1e-10)


def test_valid_rotations(example_piece):
    """Test that valid rotations are properly generated."""
    rotations = coordinate_transformations.generate_all_valid_rotations(example_piece)
    assert len(rotations) == 24
    for rotation in rotations:
        assert np.array_equal(
            rotation.positions[0], Location3D(0, 0, 0)
        )  # All rotations shall happen around origin, hence no change
