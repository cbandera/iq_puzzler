from __future__ import annotations
import numpy as np
from .coordinates import XY_DIST, Z_DIST
from .puzzle_piece import PuzzlePiece, Location3D, RotationMatrix


def is_rotation_matrix_orthogonal(rotation_matrix: RotationMatrix) -> bool:
    """Test that generated rotation matrices are proper orthogonal matrices."""
    # Test orthogonality: R.T @ R = I
    identity = rotation_matrix.T @ rotation_matrix
    if not np.allclose(identity, np.eye(3), atol=1e-10):
        return False

    # Test proper rotation: det(R) = 1
    if not np.isclose(np.linalg.det(rotation_matrix), 1, atol=1e-10):
        return False
    return True


def align_with_grid_positions(
    positions: np.ndarray, tolerance: float = 1e-10
) -> np.ndarray:
    """Align positions with the grid if they are valid, otherwise raise an exception.

    Args:
        positions: Array of positions to check and align.
        tolerance: Maximum allowed deviation from integer values.

    Returns:
        Aligned positions if they are valid grid positions.

    Raises:
        ValueError: If positions cannot be aligned to the grid.
    """
    z_factors = positions[:, 2] / Z_DIST
    if not np.all(np.abs(z_factors - np.round(z_factors)) < tolerance):
        raise ValueError("Positions cannot be aligned to the grid in Z direction")

    even_z = np.mod(z_factors, 2) == 0
    divisors = np.where(even_z[:, np.newaxis], XY_DIST, XY_DIST / 2)
    xy_factors = positions[:, :2] / divisors

    if not np.all(np.abs(xy_factors - np.round(xy_factors)) < tolerance):
        raise ValueError("Positions cannot be aligned to the grid in X/Y direction")

    aligned_xy = np.round(xy_factors) * divisors
    aligned_z = np.round(z_factors) * Z_DIST
    return np.column_stack((aligned_xy, aligned_z))


def translate(piece: PuzzlePiece, offset: np.ndarray) -> PuzzlePiece:
    """Create a new piece by applying a translation.

    Args:
        piece: The piece to translate.
        offset: The translation vector.

    Returns:
        A new PuzzlePiece with translated coordinates.
    """
    translated_points = piece.positions + offset
    return PuzzlePiece(piece.name, piece.color, translated_points)


def rotate(piece: PuzzlePiece, rotation_matrix: RotationMatrix) -> PuzzlePiece:
    """Create a new piece by applying a rotation matrix.

    Args:
        piece: The piece to rotate.
        rotation_matrix: The rotation matrix to apply.

    Returns:
        A new piece with rotated positions.

    Raises:
        ValueError: If the rotated positions cannot be aligned to the grid.
    """
    # Apply rotation matrix to all positions
    rotated_points = piece.positions @ rotation_matrix.T

    # Check if rotation resulted in valid grid positions and align them
    aligned_points = align_with_grid_positions(rotated_points)
    return PuzzlePiece(
        piece.name, piece.color, [Location3D(*pos) for pos in aligned_points]
    )


def rotation_matrix_roll(angle_deg: float) -> RotationMatrix:
    angle = np.radians(angle_deg)
    return np.array(
        [
            [1, 0, 0],
            [0, np.cos(angle), -np.sin(angle)],
            [0, np.sin(angle), np.cos(angle)],
        ]
    )


def rotation_matrix_pitch(angle_deg: float) -> RotationMatrix:
    angle = np.radians(angle_deg)
    return np.array(
        [
            [np.cos(angle), 0, np.sin(angle)],
            [0, 1, 0],
            [-np.sin(angle), 0, np.cos(angle)],
        ]
    )


def rotation_matrix_yaw(angle_deg: float) -> RotationMatrix:
    angle = np.radians(angle_deg)
    return np.array(
        [
            [np.cos(angle), -np.sin(angle), 0],
            [np.sin(angle), np.cos(angle), 0],
            [0, 0, 1],
        ]
    )


def rotation_matrix(yaw: float, pitch: float, roll: float) -> RotationMatrix:
    """Create a rotation matrix from Euler angles in yaw-pitch-roll order.

    Args:
        yaw: Rotation around Z-axis in degrees.
        pitch: Rotation around Y-axis in degrees.
        roll: Rotation around X-axis in degrees.

    Returns:
        The combined rotation matrix.
    """
    return (
        rotation_matrix_yaw(yaw)
        @ rotation_matrix_pitch(pitch)
        @ rotation_matrix_roll(roll)
    )
