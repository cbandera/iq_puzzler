from __future__ import annotations
import json
from pathlib import Path
from typing import Dict, List
from .puzzle_piece import PuzzlePiece
from . import coordinate_transformations


class PieceManager:
    """Manages puzzle pieces and their possible positions in 3D space."""

    def __init__(self, json_path: Path):
        """Initialize an empty PieceManager."""
        self._pieces: Dict[str, List[PuzzlePiece]] = {
            piece.name: coordinate_transformations.generate_all_rotated_variants(piece)
            for piece in self._load_shapes_from_json(json_path)
        }

    def _load_shapes_from_json(self, json_path: Path) -> List[PuzzlePiece]:
        pieces_data = json.loads(json_path.read_text())
        return [PuzzlePiece.from_json(piece_data) for piece_data in pieces_data]

    @property
    def pieces(self) -> Dict[str, List[PuzzlePiece]]:
        """Get all pieces with their rotations."""
        return self._pieces
