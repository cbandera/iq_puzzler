from __future__ import annotations
from typing import List, Dict, Optional, Tuple
from .coordinates import Location3D, XY_DIST, Z_DIST
from .puzzle_model import PuzzleModel


class PyramidModel(PuzzleModel):
    """Manages the mapping between 3D coordinates and position indices within the pyramid."""

    def __init__(self):
        """Initialize the pyramid model with the pyramid structure."""
        # Define the pyramid structure:
        # - 5 layers with dimensions: 5x5, 4x4, 3x3, 2x2, 1x1 (55 total positions)
        # - Each layer is shifted up by Z_DIST in z-direction
        # - Points in each layer are spaced XY_DIST apart in x/y direction
        self._build_pyramid_structure()

    def _build_pyramid_structure(self) -> None:
        """Build the pyramid structure and create mappings between indices and coordinates."""
        # Initialize mappings
        self._index_to_coord: Dict[int, Location3D] = {}
        self._coord_to_index: Dict[Location3D, int] = {}

        # Layer dimensions (from bottom to top)
        layer_dims = [(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)]

        current_index = 0
        for layer, (rows, cols) in enumerate(layer_dims):
            z = layer * Z_DIST  # Each layer is Z_DIST higher

            # Calculate offsets to center each layer
            x_offset = (5 - cols) * XY_DIST / 2
            y_offset = (5 - rows) * XY_DIST / 2

            for row in range(rows):
                for col in range(cols):
                    x = col * XY_DIST + x_offset
                    y = row * XY_DIST + y_offset
                    coord = Location3D(x, y, z)

                    self._index_to_coord[current_index] = coord
                    self._coord_to_index[coord] = current_index
                    current_index += 1

    def coord_to_index(self, coord: Location3D) -> Optional[int]:
        """Convert 3D coordinates to a position index.

        Args:
            coord: (x, y, z) coordinates.

        Returns:
            Position index if the coordinates are valid, None otherwise.
        """
        return self._coord_to_index.get(Location3D(*coord))

    def index_to_coord(self, index: int) -> Optional[Location3D]:
        """Convert a position index to 3D coordinates.

        Args:
            index: Position index.

        Returns:
            (x, y, z) coordinates if the index is valid, None otherwise.
        """
        return self._index_to_coord.get(index)

    def is_valid_index(self, index: int) -> bool:
        """Check if a position index is valid.

        Args:
            index: Position index to validate.

        Returns:
            True if the index is valid, False otherwise.
        """
        return index in self._index_to_coord

    def is_valid_coord(self, coord: Location3D) -> bool:
        """Check if 3D coordinates are within the pyramid.

        Args:
            coord: (x, y, z) coordinates to validate.

        Returns:
            True if the coordinates are valid, False otherwise.
        """
        return Location3D(*coord) in self._coord_to_index

    def get_all_indices(self) -> List[int]:
        """Get all valid position indices.

        Returns:
            List of all valid position indices.
        """
        return list(self._index_to_coord.keys())

    def get_valid_rotations(self) -> List[Tuple[float, float, float]]:
        """Get all valid rotation angle combinations.

        Returns:
            List of tuples (yaw, pitch, roll) in degrees.
        """
        return [
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
