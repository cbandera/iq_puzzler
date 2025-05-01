"""Library of puzzle pieces."""

import json
from pathlib import Path
from typing import Dict, List

from .puzzle_piece import PuzzlePiece
from .puzzle_model import PuzzleModel
from . import coordinate_transformations


class PieceLibrary:
    """Library of puzzle pieces with their rotated variants."""

    def __init__(self, library_path: Path, model: PuzzleModel):
        """Load pieces from a JSON file.

        Args:
            library_path: Path to the JSON file containing piece definitions.
            model: The puzzle model to use for determining valid rotations.
        """
        self.pieces: Dict[str, List[PuzzlePiece]] = {}
        self._model = model

        # Load pieces from JSON
        with open(library_path, "r") as f:
            piece_data = json.load(f)

        # Create pieces and their rotated variants
        for piece_info in piece_data:
            name = piece_info["name"]
            color = piece_info["color"]
            if "positions" in piece_info:
                positions = piece_info["positions"]
            else:
                # Convert grid to positions
                grid = piece_info["grid"]
                positions = []
                for i, cell in enumerate(grid):
                    if cell:
                        x = i % 4
                        y = i // 4
                        positions.append([float(x), float(y), 0.0])
            piece = PuzzlePiece(name, color, positions)
            self.pieces[name] = self._generate_variants(piece)

    def _generate_variants(self, piece: PuzzlePiece) -> List[PuzzlePiece]:
        """Generate all valid rotated variants of a piece.

        Args:
            piece: The piece to rotate.

        Returns:
            List of all valid rotations of the piece.
        """
        variants = []
        for angles in self._model.get_valid_rotations():
            rotation_matrix = coordinate_transformations.rotation_matrix(*angles)
            rotated_piece = coordinate_transformations.rotate(piece, rotation_matrix)
            variants.append(rotated_piece)
        return variants
