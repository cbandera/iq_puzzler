from pathlib import Path
import json
from typing import Dict, List
from .puzzle_piece import PuzzlePiece
from .puzzle_piece_transformer import PuzzlePieceTransformer


class PieceManager:
    """Manages puzzle pieces and their possible positions in 3D space."""

    def __init__(self, json_path: Path, scale: float = 2.0):
        """Initialize an empty PieceManager."""
        self._transformer = PuzzlePieceTransformer()
        self._pieces: Dict[str, List[PuzzlePiece]] = {
            piece.name: self._transformer.generate_all_valid_rotations(piece)
            for piece in self._load_shapes_from_json(json_path, scale)
        }

    def _load_shapes_from_json(
        self, json_path: Path, scale: float
    ) -> List[PuzzlePiece]:
        pieces_data = json.loads(json_path.read_text())
        return [
            PuzzlePiece.from_json(piece_data, scale=scale) for piece_data in pieces_data
        ]

    @property
    def pieces(self) -> Dict[str, List[PuzzlePiece]]:
        return self._pieces
