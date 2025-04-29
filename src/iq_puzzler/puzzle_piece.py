from __future__ import annotations
import numpy as np
from typing import List, NamedTuple, Optional


class Location3D(NamedTuple):
    """A 3D location in the puzzle grid."""

    x: int
    y: int
    z: int


RotationMatrix = np.ndarray


class PuzzlePiece:
    """A puzzle piece with a name, color, and positions in 3D space."""

    def __init__(self, name: str, color: str, shape: List[Location3D]):
        """Initialize a puzzle piece.

        Args:
            name: The unique name of the piece.
            color: The color of the piece.
            shape: List of 3D locations occupied by the piece.
        """
        self.name = name
        self.color = color
        # Store positions as Nx3 numpy array with float64 for rotation calculations
        self._positions = np.array(shape, dtype=np.float64)

    def get_positions(self) -> List[Location3D]:
        """Get the list of positions occupied by this piece.

        Returns:
            List of Location3D tuples representing the piece's positions.
            Note: Positions are rounded to nearest integer to ensure grid alignment.
        """
        # Round to nearest integer when returning positions
        rounded = np.round(self._positions).astype(np.int32)
        return [Location3D(*pos) for pos in rounded]

    def is_valid_grid_position(self, tolerance: float = 1e-10) -> bool:
        """Check if all positions are effectively integers.

        Args:
            tolerance: Maximum allowed deviation from integer values.

        Returns:
            True if all coordinates are within tolerance of integer values.
        """
        return np.allclose(self._positions, np.round(self._positions), atol=tolerance)

    def translated(self, offset: Location3D) -> PuzzlePiece:
        """Create a new piece by translating this piece by the given offset.

        Args:
            offset: The translation vector to apply.

        Returns:
            A new PuzzlePiece with translated coordinates.
        """
        translated_points = self._positions + np.array([offset.x, offset.y, offset.z])
        return PuzzlePiece(
            self.name,
            self.color,
            [
                Location3D(int(round(x)), int(round(y)), int(round(z)))
                for x, y, z in translated_points
            ],
        )

    def rotated(self, rotation_matrix: RotationMatrix) -> Optional[PuzzlePiece]:
        """Create a new piece by applying a rotation matrix.

        Args:
            rotation_matrix: 3x3 rotation matrix to apply.

        Returns:
            A new PuzzlePiece if the rotation results in valid grid positions,
            None otherwise.
        """
        if rotation_matrix.shape != (3, 3):
            raise ValueError("Rotation matrix must be 3x3")

        # Apply rotation
        rotated_points = self._positions @ rotation_matrix.T

        # Create new piece with rotated points
        rotated = PuzzlePiece(
            self.name,
            self.color,
            [
                Location3D(int(round(x)), int(round(y)), int(round(z)))
                for x, y, z in rotated_points
            ],
        )

        # Check if rotation resulted in valid grid positions
        if not rotated.is_valid_grid_position():
            return None

        return rotated

    @classmethod
    def from_json(cls, json_data: dict, scale: float = 2.0) -> PuzzlePiece:
        """Create a piece from JSON data.

        Args:
            json_data: Dictionary containing piece data.
            scale: Scaling factor to apply to coordinates.

        Returns:
            A new PuzzlePiece instance.
        """
        name = json_data["name"]
        color = json_data["color"]
        grid = json_data["grid"]

        # Convert the flat grid array into scaled (x, y) coordinates
        # where grid[y * 4 + x] is True
        coordinates = []
        for y in range(4):
            for x in range(4):
                if grid[y * 4 + x]:
                    coordinates.append(Location3D(int(x * scale), int(y * scale), 0))

        return cls(name, color, coordinates)
