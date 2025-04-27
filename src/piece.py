from typing import List, Tuple, Dict

class Piece2D:
    """Represents a 2D puzzle piece in its local coordinate system."""
    
    def __init__(self, name: str, color: str, shape: List[Tuple[int, int]]):
        """Initialize a 2D piece.
        
        Args:
            name: Unique identifier for the piece.
            color: RGB color string for visualization.
            shape: List of (x, y) coordinates defining the piece's shape.
        """
        self._name = name
        self._color = color
        self._shape = shape
    
    @property
    def name(self) -> str:
        """Get the piece's name."""
        return self._name
    
    @property
    def color(self) -> str:
        """Get the piece's color."""
        return self._color
    
    def get_shape(self) -> List[Tuple[int, int]]:
        """Get the piece's shape as a list of (x, y) coordinates."""
        return self._shape.copy()
    
    @classmethod
    def from_json(cls, json_data: dict, scale: float = 2.0) -> 'Piece2D':
        """Create a Piece2D instance from JSON data.
        
        Args:
            json_data: Dictionary containing piece data with keys:
                - name: Piece name
                - color: RGB color string
                - grid: 4x4 boolean grid defining piece shape
            scale: Scaling factor to apply to coordinates (default: 2.0)
        
        Returns:
            A new Piece2D instance.
        """
        name = json_data["name"]
        color = json_data["color"]
        grid = json_data["grid"]
        
        # Convert the flat grid array into scaled (x, y) coordinates
        # where grid[y * 4 + x] is True
        shape = []
        for y in range(4):
            for x in range(4):
                if grid[y * 4 + x]:
                    shape.append((int(x * scale), int(y * scale)))
        
        return cls(name, color, shape)
