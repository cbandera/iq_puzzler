from __future__ import annotations
import numpy as np
from typing import List
from .puzzle_piece import PuzzlePiece, RotationMatrix


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

    def _compute_rotation_matrices(self) -> List[RotationMatrix]:
        """Precompute all possible rotation matrices for 3D positioning."""

        def rotation_matrix_x(angle_deg: float) -> RotationMatrix:
            angle = np.radians(angle_deg)
            return np.array(
                [
                    [1, 0, 0],
                    [0, np.cos(angle), -np.sin(angle)],
                    [0, np.sin(angle), np.cos(angle)],
                ]
            )

        def rotation_matrix_y(angle_deg: float) -> RotationMatrix:
            angle = np.radians(angle_deg)
            return np.array(
                [
                    [np.cos(angle), 0, np.sin(angle)],
                    [0, 1, 0],
                    [-np.sin(angle), 0, np.cos(angle)],
                ]
            )

        def rotation_matrix_z(angle_deg: float) -> RotationMatrix:
            angle = np.radians(angle_deg)
            return np.array(
                [
                    [np.cos(angle), -np.sin(angle), 0],
                    [np.sin(angle), np.cos(angle), 0],
                    [0, 0, 1],
                ]
            )

        rotation_matrices = []
        for yaw, pitch, roll in self._valid_rotations:
            # Apply rotations in yaw-pitch-roll order
            Rz = rotation_matrix_z(yaw)
            Ry = rotation_matrix_y(pitch)
            Rx = rotation_matrix_x(roll)
            R = Rx @ Ry @ Rz  # Matrix multiplication
            rotation_matrices.append(R)
        return rotation_matrices

    def generate_all_valid_rotations(self, piece: PuzzlePiece) -> List[PuzzlePiece]:
        return list(
            filter(
                None,
                [
                    piece.rotated(rotation_matrix)
                    for rotation_matrix in self._rotation_matrices
                ],
            )
        )
