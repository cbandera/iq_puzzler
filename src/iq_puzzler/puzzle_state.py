from dataclasses import dataclass
from typing import Dict, Set, List, Optional
import json

from iq_puzzler import coordinate_transformations
from .puzzle_model import PuzzleModel
from .puzzle_piece import PuzzlePiece


@dataclass
class PiecePlacement:
    """Represents the placement of a piece in the puzzle."""

    piece: PuzzlePiece
    occupied_indices: Set[int]  # Set of position indices occupied by this piece


class PuzzleState:
    """Manages the current state of the puzzle, tracking placed pieces and their positions."""

    def __init__(self, model: PuzzleModel):
        """Initialize an empty puzzle state."""
        self._model: PuzzleModel = model
        self._placements: Dict[
            str, PiecePlacement
        ] = {}  # Map piece name to its placement
        self._occupied_indices: Set[int] = set()  # Set of all occupied position indices

    def place_piece(
        self,
        piece: PuzzlePiece,
        position_index: int,
    ) -> bool:
        """Place a piece in the puzzle.

        Args:
            piece: The piece to place.
            position_index: The integer index of the piece's origin position.

        Returns:
            bool: True if the piece was placed successfully, False if the placement would
                cause an overlap or the piece is already placed.
        """
        # Check if piece is already placed
        if piece.name in self._placements:
            return False

        # Move piece to the specified position
        origin = self._model.index_to_coord(position_index)
        placed_piece = coordinate_transformations.translate(piece, origin)

        # Check if piece positions are valid
        if not all(
            self._model.is_valid_coord(coord) for coord in placed_piece.positions
        ):
            return False
        piece_indices = set(
            self._model.coord_to_index(coord) for coord in placed_piece.positions
        )

        # Check for overlap with existing pieces
        if self._occupied_indices.intersection(piece_indices):
            return False

        # Add the placement
        placement = PiecePlacement(
            piece=placed_piece,
            occupied_indices=piece_indices,
        )
        self._placements[piece.name] = placement
        self._occupied_indices.update(piece_indices)
        return True

    def remove_piece(self, name: str) -> bool:
        """Remove a piece from the puzzle.

        Args:
            name: The name of the piece to remove.

        Returns:
            bool: True if the piece was removed, False if it wasn't placed.
        """
        placement = self._placements.get(name)
        if placement is None:
            return False

        self._occupied_indices.difference_update(placement.occupied_indices)
        del self._placements[name]
        return True

    def get_placement(self, name: str) -> Optional[PiecePlacement]:
        """Get the placement information for a piece.

        Args:
            name: The name of the piece.

        Returns:
            The PiecePlacement if the piece is placed, None otherwise.
        """
        return self._placements.get(name)

    def get_occupied_indices(self) -> Set[int]:
        """Return the set of all occupied position indices."""
        return self._occupied_indices.copy()

    def get_placements(self) -> List[PiecePlacement]:
        """Get all current piece placements.

        Returns:
            List of all piece placements.
        """
        return list(self._placements.values())

    def is_piece_placed(self, name: str) -> bool:
        """Check if a piece is currently placed in the puzzle.

        Args:
            name: The name string of the piece.

        Returns:
            bool: True if the piece is placed, False otherwise.
        """
        return name in self._placements

    def export_to_json(self, filepath: str) -> None:
        """Export the current puzzle state to a JSON file.

        The export contains all possible position indices, their 3D coordinates,
        and information about pieces occupying those positions.

        Args:
            filepath: Path where to save the JSON file
        """
        grid_data = {}

        # Export all possible positions
        for idx in self._model.get_all_indices():
            coord = self._model.index_to_coord(idx)
            position_data = {
                "coordinate": {
                    "x": float(coord.x),
                    "y": float(coord.y),
                    "z": float(coord.z),
                },
                "occupied": False,
                "piece_name": None,
                "piece_color": None,
            }

            # Check if position is occupied
            for name, placement in self._placements.items():
                if idx in placement.occupied_indices:
                    position_data["occupied"] = True
                    position_data["piece_name"] = name
                    position_data["piece_color"] = placement.piece.color
                    break

            grid_data[str(idx)] = position_data

        # Write to file
        with open(filepath, "w") as f:
            json.dump(grid_data, f, indent=2)
