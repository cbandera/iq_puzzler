from __future__ import annotations
import numpy as np
from typing import List, Optional
from .puzzle_piece import PuzzlePiece, Location3D, RotationMatrix

XY_DIST = 1.0
Z_DIST = 0.5 * np.sqrt(
    2 * XY_DIST * XY_DIST
)  # Half the hypothenuse of a right triangle with legs of length XY_DIST


def align_with_grid_positions(
    positions: np.ndarray, tolerance: float = 1e-10
) -> Optional[np.ndarray]:
    """Align positions with the grid if they are valid, otherwise return None.

    Args:
        positions: Array of positions to check and align.
        tolerance: Maximum allowed deviation from integer values.

    Returns:
        Aligned positions if they are valid grid positions, None otherwise.
    """
    z_factors = positions[:, 2] / Z_DIST
    if not np.all(np.abs(z_factors - np.round(z_factors)) < tolerance):
        return None

    even_z = np.mod(z_factors, 2) == 0
    divisors = np.where(even_z[:, np.newaxis], XY_DIST, XY_DIST / 2)
    xy_factors = positions[:, :2] / divisors

    if not np.all(np.abs(xy_factors - np.round(xy_factors)) < tolerance):
        return None

    aligned_xy = np.round(xy_factors) * divisors
    aligned_z = np.round(z_factors) * Z_DIST
    return np.column_stack((aligned_xy, aligned_z))


def translate(piece: PuzzlePiece, offset: Location3D) -> PuzzlePiece:
    """Create a new piece by applying a translation.

    Args:
        piece: The piece to translate.
        offset: The translation vector.

    Returns:
        A new PuzzlePiece with translated coordinates.
    """
    translated_points = piece.positions + np.array([offset.x, offset.y, offset.z])
    return PuzzlePiece(
        piece.name, piece.color, [Location3D(*pos) for pos in translated_points]
    )


def rotate(
    piece: PuzzlePiece, rotation_matrix: RotationMatrix
) -> Optional[PuzzlePiece]:
    """Create a new piece by applying a rotation matrix.

    Args:
        piece: The piece to rotate.
        rotation_matrix: 3x3 rotation matrix to apply.

    Returns:
        A new PuzzlePiece if the rotation results in valid grid positions,
        None otherwise.
    """
    if rotation_matrix.shape != (3, 3):
        raise ValueError("Rotation matrix must be 3x3")

    # Apply rotation
    rotated_points = piece.positions @ rotation_matrix.T

    # Check if rotation resulted in valid grid positions
    aligned_points = align_with_grid_positions(rotated_points)
    if aligned_points is not None:
        return PuzzlePiece(
            piece.name, piece.color, [Location3D(*pos) for pos in aligned_points]
        )
    else:
        return None


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
    """Create a rotation matrix from Euler angles in yaw-pitch-roll order."""
    Rz = rotation_matrix_yaw(yaw)
    Ry = rotation_matrix_pitch(pitch)
    Rx = rotation_matrix_roll(roll)
    return Rz @ Ry @ Rx


_VALID_ROTATIONS = [
    # Flat options: These involve rotations around the Z-axis (yaw) and rotations
    # of 0° and 180° around the X-axis. No rotation around the Y-axis.
    (0, 0, 0),
    (90, 0, 0),
    (180, 0, 0),
    (270, 0, 0),
    (0, 0, 180),
    (90, 0, 180),
    (180, 0, 180),
    (270, 0, 180),
    # 3D rotations: These involve 4 rotations around the Z-axis (starting at 45°
    # with 90° increments), combined with two angles around the Y-axis (+/- 45°)
    # and two angles around the X-axis (+/- 90°).
    (45, 45, 90),
    (45, 45, -90),
    (45, -45, 90),
    (45, -45, -90),
    (135, 45, 90),
    (135, 45, -90),
    (135, -45, 90),
    (135, -45, -90),
    (225, 45, 90),
    (225, 45, -90),
    (225, -45, 90),
    (225, -45, -90),
    (315, 45, 90),
    (315, 45, -90),
    (315, -45, 90),
    (315, -45, -90),
]


def _compute_rotation_matrices() -> List[RotationMatrix]:
    """Precompute all possible rotation matrices for 3D positioning."""
    rotation_matrices = []
    for yaw, pitch, roll in _VALID_ROTATIONS:
        R = rotation_matrix(yaw, pitch, roll)
        rotation_matrices.append(R)
    return rotation_matrices


_ROTATION_MATRICES = _compute_rotation_matrices()


def generate_all_valid_rotations(piece: PuzzlePiece) -> List[PuzzlePiece]:
    """Generate all valid rotations of a piece.

    Args:
        piece: The piece to rotate.

    Returns:
        A list of all valid rotations of the piece.
    """
    return list(
        filter(
            None,
            [rotate(piece, rotation_matrix) for rotation_matrix in _ROTATION_MATRICES],
        )
    )
