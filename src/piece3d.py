from typing import List, Tuple, Dict
import numpy as np
from .piece import Piece2D

class Piece3D:
    """Represents a 3D transformation of a 2D piece with its valid variants."""
    
    def __init__(self, piece2d: Piece2D):
        """Initialize a 3D piece from a 2D piece.
        
        Args:
            piece2d: The 2D piece to transform.
        """
        self._piece2d = piece2d
        self._variants: Dict[int, np.ndarray] = {
            0: np.array([(x, y, 0) for x, y in piece2d.get_shape()])
        }
    
    @property
    def name(self) -> str:
        """Get the piece's name."""
        return self._piece2d.name
    
    @property
    def color(self) -> str:
        """Get the piece's color."""
        return self._piece2d.color
    
    def get_variant_indices(self) -> List[int]:
        """Get the list of valid variant indices for this piece.
        
        Returns:
            List of valid variant indices.
        """
        return list(self._variants.keys())
    
    def get_variant(self, variant_index: int) -> np.ndarray:
        """Get the 3D coordinates for a specific variant.
        
        Args:
            variant_index: Index of the desired variant.
        
        Returns:
            Array of (x, y, z) coordinates for the variant.
        
        Raises:
            KeyError: If the variant index is not valid.
        """
        if variant_index not in self._variants:
            raise KeyError(f"Invalid variant index {variant_index} for piece {self.name}")
        return self._variants[variant_index].copy()
    
    def set_variants(self, variants: Dict[int, np.ndarray]) -> None:
        """Set the valid variants for this piece.
        
        Args:
            variants: Dictionary mapping variant indices to their 3D coordinate arrays.
        """
        self._variants = variants
