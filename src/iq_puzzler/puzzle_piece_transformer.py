from __future__ import annotations
import numpy as np
from typing import List, Optional
from .puzzle_piece import PuzzlePiece, Location3D, RotationMatrix


class PuzzlePieceTransformer:
    """Handles geometric transformations of puzzle pieces."""

    def __init__(self):
        """Initialize the transformer with precomputed rotation matrices."""
        self._valid_rotations = [
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
        self._rotation_matrices: List[RotationMatrix] = (
            self._compute_rotation_matrices()
        )

    @staticmethod
    def _is_valid_grid_position(
        positions: np.ndarray, tolerance: float = 1e-10
    ) -> bool:
        """Check if all positions are effectively integers.

        Args:
            positions: Array of positions to check.
            tolerance: Maximum allowed deviation from integer values.

        Returns:
            True if all positions are within tolerance of integer values.
        """
        return np.all(np.abs(np.round(positions) - positions) < tolerance)

    @staticmethod
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

    @staticmethod
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
        if PuzzlePieceTransformer._is_valid_grid_position(rotated_points):
            # Create new piece with rounded integer positions
            return PuzzlePiece(
                piece.name,
                piece.color,
                [
                    Location3D(int(round(x)), int(round(y)), int(round(z)))
                    for x, y, z in rotated_points
                ],
            )
        else:
            return None

    @staticmethod
    def rotation_matrix_roll(angle_deg: float) -> RotationMatrix:
        angle = np.radians(angle_deg)
        return np.array(
            [
                [1, 0, 0],
                [0, np.cos(angle), -np.sin(angle)],
                [0, np.sin(angle), np.cos(angle)],
            ]
        )

    @staticmethod
    def rotation_matrix_pitch(angle_deg: float) -> RotationMatrix:
        angle = np.radians(angle_deg)
        return np.array(
            [
                [np.cos(angle), 0, np.sin(angle)],
                [0, 1, 0],
                [-np.sin(angle), 0, np.cos(angle)],
            ]
        )

    @staticmethod
    def rotation_matrix_yaw(angle_deg: float) -> RotationMatrix:
        angle = np.radians(angle_deg)
        return np.array(
            [
                [np.cos(angle), -np.sin(angle), 0],
                [np.sin(angle), np.cos(angle), 0],
                [0, 0, 1],
            ]
        )

    @staticmethod
    def rotation_matrix(yaw: float, pitch: float, roll: float) -> RotationMatrix:
        """Create a rotation matrix from Euler angles in yaw-pitch-roll order."""
        # Apply rotations in yaw-pitch-roll order
        Rz = PuzzlePieceTransformer.rotation_matrix_yaw(yaw)
        Ry = PuzzlePieceTransformer.rotation_matrix_pitch(pitch)
        Rx = PuzzlePieceTransformer.rotation_matrix_roll(roll)
        return Rz @ Ry @ Rx

    def _compute_rotation_matrices(self) -> List[RotationMatrix]:
        """Precompute all possible rotation matrices for 3D positioning."""
        rotation_matrices = []
        for yaw, pitch, roll in self._valid_rotations:
            R = PuzzlePieceTransformer.rotation_matrix(yaw, pitch, roll)
            rotation_matrices.append(R)
        return rotation_matrices

    def generate_all_valid_rotations(self, piece: PuzzlePiece) -> List[PuzzlePiece]:
        return list(
            filter(
                None,
                [
                    self.rotate(piece, rotation_matrix)
                    for rotation_matrix in self._rotation_matrices
                ],
            )
        )
