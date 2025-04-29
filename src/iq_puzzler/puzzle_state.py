from dataclasses import dataclass
from typing import Dict, Set, List, Optional


@dataclass
class PiecePlacement:
    """Represents the placement of a piece in the puzzle."""

    color: str
    position_index: int
    orientation_index: int
    occupied_indices: Set[int]  # Set of position indices occupied by this piece


class PuzzleState:
    """Manages the current state of the puzzle, tracking placed pieces and their positions."""

    def __init__(self):
        """Initialize an empty puzzle state."""
        self._placements: Dict[
            str, PiecePlacement
        ] = {}  # Map piece color to its placement
        self._occupied_indices: Set[int] = set()  # Set of all occupied position indices

    def place_piece(
        self,
        color: str,
        position_index: int,
        orientation_index: int,
        occupied_indices: Set[int],
    ) -> bool:
        """Place a piece in the puzzle.

        Args:
            color: The RGB color string of the piece.
            position_index: The integer index of the piece's origin position.
            orientation_index: The orientation index specifying the piece's rotation.
            occupied_indices: Set of position indices that this piece will occupy.

        Returns:
            bool: True if the piece was placed successfully, False if the placement would
                cause an overlap or the piece is already placed.
        """
        # Check if piece is already placed
        if color in self._placements:
            return False

        # Check for overlap with existing pieces
        if self._occupied_indices.intersection(occupied_indices):
            return False

        # Add the placement
        placement = PiecePlacement(
            color=color,
            position_index=position_index,
            orientation_index=orientation_index,
            occupied_indices=occupied_indices,
        )
        self._placements[color] = placement
        self._occupied_indices.update(occupied_indices)
        return True

    def remove_piece(self, color: str) -> bool:
        """Remove a piece from the puzzle.

        Args:
            color: The RGB color string of the piece to remove.

        Returns:
            bool: True if the piece was removed, False if it wasn't placed.
        """
        placement = self._placements.get(color)
        if placement is None:
            return False

        self._occupied_indices.difference_update(placement.occupied_indices)
        del self._placements[color]
        return True

    def get_placement(self, color: str) -> Optional[PiecePlacement]:
        """Get the placement information for a piece.

        Args:
            color: The RGB color string of the piece.

        Returns:
            The PiecePlacement if the piece is placed, None otherwise.
        """
        return self._placements.get(color)

    def get_occupied_indices(self) -> Set[int]:
        """Get all position indices that are currently occupied.

        Returns:
            Set of occupied position indices.
        """
        return self._occupied_indices.copy()

    def get_placed_pieces(self) -> List[PiecePlacement]:
        """Get information about all placed pieces.

        Returns:
            List of PiecePlacement objects for all placed pieces.
        """
        return list(self._placements.values())

    def is_piece_placed(self, color: str) -> bool:
        """Check if a piece is currently placed in the puzzle.

        Args:
            color: The RGB color string of the piece.

        Returns:
            bool: True if the piece is placed, False otherwise.
        """
        return color in self._placements
