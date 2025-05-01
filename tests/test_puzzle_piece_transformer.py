from iq_puzzler.puzzle_piece_transformer import PuzzlePieceTransformer
from iq_puzzler.puzzle_piece import PuzzlePiece, Location3D
import numpy as np


def test_puzzle_transformer_initialization():
    transformer = PuzzlePieceTransformer()
    assert len(transformer._rotation_matrices) == 24
    assert np.array_equal(
        transformer._rotation_matrices[0], np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    )


def test_puzzle_transformer_generate_all_valid_rotations():
    transformer = PuzzlePieceTransformer()
    piece = PuzzlePiece(
        "Test",
        "rgb(255, 0, 0)",
        [
            Location3D(0, 0, 0),
            Location3D(2, 0, 0),
            Location3D(4, 0, 0),
            Location3D(4, 2, 0),
        ],
    )
    rotations = transformer.generate_all_valid_rotations(piece)
    assert len(rotations) == 8
    for rotation in rotations:
        assert np.array_equal(
            rotation.positions[0], Location3D(0, 0, 0)
        )  # All rotations shall happen around origin, hence no change

    # Test some of the rotations
    assert np.array_equal(  # (0, 0, 0),
        rotations[0].positions,
        [
            Location3D(0, 0, 0),
            Location3D(2, 0, 0),
            Location3D(4, 0, 0),
            Location3D(4, 2, 0),
        ],
    )
    assert np.array_equal(  # (90, 0, 0),
        rotations[1].positions,
        [
            Location3D(0, 0, 0),
            Location3D(0, 2, 0),
            Location3D(0, 4, 0),
            Location3D(-2, 4, 0),
        ],
    )
    assert np.array_equal(  # (180, 0, 0),
        rotations[2].positions,
        [
            Location3D(0, 0, 0),
            Location3D(-2, 0, 0),
            Location3D(-4, 0, 0),
            Location3D(-4, -2, 0),
        ],
    )
    assert np.array_equal(  # (270, 0, 0),
        rotations[3].positions,
        [
            Location3D(0, 0, 0),
            Location3D(0, -2, 0),
            Location3D(0, -4, 0),
            Location3D(2, -4, 0),
        ],
    )
    assert np.array_equal(  # (0, 0, 180),
        rotations[4].positions,
        [
            Location3D(0, 0, 0),
            Location3D(2, 0, 0),
            Location3D(4, 0, 0),
            Location3D(4, -2, 0),
        ],
    )
    assert np.array_equal(  # (90, 0, 180),
        rotations[5].positions,
        [
            Location3D(0, 0, 0),
            Location3D(0, 2, 0),
            Location3D(0, 4, 0),
            Location3D(2, 4, 0),
        ],
    )
    assert np.array_equal(  # (180, 0, 180),
        rotations[6].positions,
        [
            Location3D(0, 0, 0),
            Location3D(-2, 0, 0),
            Location3D(-4, 0, 0),
            Location3D(-4, 2, 0),
        ],
    )
    assert np.array_equal(  # (270, 0, 180),
        rotations[7].positions,
        [
            Location3D(0, 0, 0),
            Location3D(0, -2, 0),
            Location3D(0, -4, 0),
            Location3D(-2, -4, 0),
        ],
    )
    # assert np.array_equal(  # (45, -45, 90),
    #     rotations[10].positions,
    #     [
    #         Location3D(0, 0, 0),
    #         Location3D(1, 1, 1),
    #         Location3D(2, 2, 2),
    #         Location3D(1, 1, 3),
    #     ],
    # )


def test_rotation_matrix_orthogonality():
    """Test that generated rotation matrices are proper orthogonal matrices."""
    transformer = PuzzlePieceTransformer()

    # Test some specific angles
    test_angles = [
        (0, 0, 0),  # Identity
        (90, 0, 0),  # Pure yaw
        (0, 90, 0),  # Pure pitch
        (0, 0, 90),  # Pure roll
        (45, 45, 90),  # Mixed rotation
    ]

    for yaw, pitch, roll in test_angles:
        R = transformer.rotation_matrix(yaw, pitch, roll)

        # Test R * R^T = I
        I = np.eye(3)
        assert np.allclose(
            R @ R.T, I
        ), f"Non-orthogonal matrix for angles ({yaw}, {pitch}, {roll})"

        # Test determinant = 1
        assert np.isclose(
            np.linalg.det(R), 1.0
        ), f"Non-proper rotation for angles ({yaw}, {pitch}, {roll})"

        # Test that distances are preserved (for a unit vector)
        v = np.array([1.0, 0.0, 0.0])
        rotated_v = R @ v
        assert np.isclose(
            np.linalg.norm(rotated_v), 1.0
        ), f"Length not preserved for angles ({yaw}, {pitch}, {roll})"
