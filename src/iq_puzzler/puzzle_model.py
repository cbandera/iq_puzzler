"""Interface for puzzle models that map coordinates to indices."""

from __future__ import annotations
from typing import List, Optional, Tuple
from abc import ABC, abstractmethod
from .coordinates import Location3D


class PuzzleModel(ABC):
    """Interface for managing the mapping between 3D coordinates and position indices within a puzzle."""

    @abstractmethod
    def coord_to_index(self, coord: Location3D) -> Optional[int]:
        """Convert 3D coordinates to a position index.

        Args:
            coord: (x, y, z) coordinates.

        Returns:
            Position index if the coordinates are valid, None otherwise.
        """
        pass

    @abstractmethod
    def index_to_coord(self, index: int) -> Optional[Location3D]:
        """Convert a position index to 3D coordinates.

        Args:
            index: Position index.

        Returns:
            (x, y, z) coordinates if the index is valid, None otherwise.
        """
        pass

    @abstractmethod
    def is_valid_index(self, index: int) -> bool:
        """Check if a position index is valid.

        Args:
            index: Position index to validate.

        Returns:
            True if the index is valid, False otherwise.
        """
        pass

    @abstractmethod
    def is_valid_coord(self, coord: Location3D) -> bool:
        """Check if 3D coordinates are within the puzzle.

        Args:
            coord: (x, y, z) coordinates to validate.

        Returns:
            True if the coordinates are valid, False otherwise.
        """
        pass

    @abstractmethod
    def get_all_indices(self) -> List[int]:
        """Get all valid position indices.

        Returns:
            List of all valid position indices.
        """
        pass

    @abstractmethod
    def get_valid_rotations(self) -> List[Tuple[float, float, float]]:
        """Get all valid rotation angle combinations.

        Returns:
            List of tuples (yaw, pitch, roll) in degrees.
        """
        pass
