from __future__ import annotations
import numpy as np
from typing import List, NamedTuple


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
        self.positions = np.array(shape, dtype=np.float64)

    @classmethod
    def from_json(cls, json_data: dict) -> PuzzlePiece:
        """Create a piece from JSON data.

        Args:
            json_data: Dictionary containing piece data.

        Returns:
            A new PuzzlePiece instance.
        """
        name = json_data["name"]
        color = json_data["color"]
        grid = json_data["grid"]

        # Convert the flat grid array into (x, y) coordinates
        # where grid[y * 4 + x] is True
        coordinates = []
        for y in range(4):
            for x in range(4):
                if grid[y * 4 + x]:
                    coordinates.append(Location3D(x, y, 0))

        return cls(name, color, coordinates)
