from typing import List, Tuple, Dict, Optional
import numpy as np

class PositionValidator:
    """Manages the mapping between 3D coordinates and position indices within the pyramid."""
    
    def __init__(self):
        """Initialize the position validator with the pyramid structure."""
        # Define the pyramid structure:
        # - 5 layers
        # - Each layer is shifted up by 1 unit
        # - Base layer is a 4x4 grid
        self._build_pyramid_structure()
    
    def _build_pyramid_structure(self) -> None:
        """Build the pyramid structure and create mappings between indices and coordinates."""
        # Initialize mappings
        self._index_to_coord: Dict[int, Tuple[float, float, float]] = {}
        self._coord_to_index: Dict[Tuple[float, float, float], int] = {}
        
        # Layer dimensions (from bottom to top)
        layer_dims = [(4, 4), (3, 3), (2, 2), (2, 1), (1, 1)]
        
        current_index = 0
        for layer, (rows, cols) in enumerate(layer_dims):
            z = layer * 1.0  # Each layer is 1 unit higher
            
            # Calculate offsets to center each layer
            x_offset = (4 - cols) / 2.0
            y_offset = (4 - rows) / 2.0
            
            for row in range(rows):
                for col in range(cols):
                    x = col + x_offset
                    y = row + y_offset
                    coord = (x, y, z)
                    
                    self._index_to_coord[current_index] = coord
                    self._coord_to_index[coord] = current_index
                    current_index += 1
    
    def coord_to_index(self, coord: Tuple[float, float, float]) -> Optional[int]:
        """Convert 3D coordinates to a position index.
        
        Args:
            coord: (x, y, z) coordinates.
        
        Returns:
            Position index if the coordinates are valid, None otherwise.
        """
        # Round coordinates to handle floating-point imprecision
        rounded = tuple(round(c, 6) for c in coord)
        return self._coord_to_index.get(rounded)
    
    def index_to_coord(self, index: int) -> Optional[Tuple[float, float, float]]:
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
    
    def is_valid_coord(self, coord: Tuple[float, float, float]) -> bool:
        """Check if 3D coordinates are within the pyramid.
        
        Args:
            coord: (x, y, z) coordinates to validate.
        
        Returns:
            True if the coordinates are valid, False otherwise.
        """
        # Round coordinates to handle floating-point imprecision
        rounded = tuple(round(c, 6) for c in coord)
        return rounded in self._coord_to_index
    
    def get_all_indices(self) -> List[int]:
        """Get all valid position indices.
        
        Returns:
            List of all valid position indices.
        """
        return list(self._index_to_coord.keys())
