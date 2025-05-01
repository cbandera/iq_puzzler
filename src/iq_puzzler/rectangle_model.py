"""Rectangle model implementation."""
from typing import List, Optional

from .coordinates import Location3D
from .puzzle_model import PuzzleModel


class RectangleModel(PuzzleModel):
    """Model for the rectangular game board configuration."""

    def coord_to_index(self, coord: Location3D) -> Optional[int]:
        """Convert coordinates to index."""
        raise NotImplementedError("Rectangle mode not implemented yet")

    def index_to_coord(self, index: int) -> Optional[Location3D]:
        """Convert index to coordinates."""
        raise NotImplementedError("Rectangle mode not implemented yet")

    def is_valid_index(self, index: int) -> bool:
        """Check if index is valid."""
        raise NotImplementedError("Rectangle mode not implemented yet")

    def is_valid_coord(self, coord: Location3D) -> bool:
        """Check if coordinates are valid."""
        raise NotImplementedError("Rectangle mode not implemented yet")

    def get_all_indices(self) -> List[int]:
        """Get all valid indices."""
        raise NotImplementedError("Rectangle mode not implemented yet")
