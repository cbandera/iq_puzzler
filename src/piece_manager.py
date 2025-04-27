import json
import numpy as np
from typing import Dict, List, Tuple, Optional, Set
from .piece import Piece

class PieceManager:
    """Manages the puzzle pieces and their transformations."""
    
    def __init__(self):
        """Initialize an empty PieceManager."""
        self._pieces: Dict[str, Piece] = {}  # Map piece name to Piece instance
        self._rotation_matrices: Dict[int, np.ndarray] = {}  # Map rotation index to 3x3 matrix
        self._compute_rotation_matrices()
    
    def _compute_rotation_matrices(self) -> None:
        """Precompute all possible rotation matrices.
        
        This creates 24 rotation matrices from combinations of:
        - Z-axis rotations (0°, 90°, 180°, 270°)
        - Y-axis rotations (0°, ±45°)
        - X-axis rotations (0°, ±90°, 180°)
        """
        def rotation_matrix_x(angle_deg: float) -> np.ndarray:
            angle = np.radians(angle_deg)
            return np.array([
                [1, 0, 0],
                [0, np.cos(angle), -np.sin(angle)],
                [0, np.sin(angle), np.cos(angle)]
            ])

        def rotation_matrix_y(angle_deg: float) -> np.ndarray:
            angle = np.radians(angle_deg)
            return np.array([
                [np.cos(angle), 0, np.sin(angle)],
                [0, 1, 0],
                [-np.sin(angle), 0, np.cos(angle)]
            ])

        def rotation_matrix_z(angle_deg: float) -> np.ndarray:
            angle = np.radians(angle_deg)
            return np.array([
                [np.cos(angle), -np.sin(angle), 0],
                [np.sin(angle), np.cos(angle), 0],
                [0, 0, 1]
            ])

        z_angles = [0, 90, 180, 270]
        y_angles = [0, 45, -45]
        x_angles = [0, 90, -90, 180]

        rotation_idx = 0
        for z in z_angles:
            for y in y_angles:
                for x in x_angles:
                    # Apply rotations in Z-Y-X order
                    Rz = rotation_matrix_z(z)
                    Ry = rotation_matrix_y(y)
                    Rx = rotation_matrix_x(x)
                    R = Rx @ Ry @ Rz  # Matrix multiplication
                    self._rotation_matrices[rotation_idx] = R
                    rotation_idx += 1
    
    def _compute_piece_variants(self, piece: Piece) -> None:
        """Compute all valid variants for a piece by applying rotation matrices.
        
        A variant is considered valid if all resulting coordinates are integers.
        
        Args:
            piece: The piece to compute variants for.
        """
        base_shape = piece.get_shape()
        valid_variants = {0: base_shape}  # Base variant is always valid
        
        # Convert 2D coordinates to 3D (z=0)
        points_3d = np.array([(x, y, 0) for x, y in base_shape])
        
        for rot_idx, matrix in self._rotation_matrices.items():
            # Apply rotation to all points
            rotated_points = points_3d @ matrix.T  # Use transpose for point transformation
            
            # Check if all coordinates are (approximately) integers
            if np.allclose(rotated_points, np.round(rotated_points), atol=1e-10):
                # Convert back to 2D coordinates (ignore z)
                variant_shape = [(int(round(x)), int(round(y))) 
                               for x, y, _ in rotated_points.tolist()]
                
                # Only add unique variants
                variant_tuple = tuple(sorted(variant_shape))
                if not any(tuple(sorted(v)) == variant_tuple 
                         for v in valid_variants.values()):
                    valid_variants[len(valid_variants)] = variant_shape
        
        piece.set_variants(valid_variants)
    
    def load_pieces_from_json(self, json_path: str, scale: float = 2.0) -> None:
        """Load piece definitions from a JSON file.
        
        Args:
            json_path: Path to the JSON file containing piece definitions.
            scale: Scaling factor to apply to piece coordinates (default: 2.0).
        
        Raises:
            FileNotFoundError: If the JSON file doesn't exist.
            json.JSONDecodeError: If the JSON file is invalid.
        """
        with open(json_path, 'r') as f:
            pieces_data = json.load(f)
        
        for piece_data in pieces_data:
            piece = Piece.from_json(piece_data, scale=scale)
            self._pieces[piece.name] = piece
            self._compute_piece_variants(piece)
    
    def get_piece_by_name(self, name: str) -> Optional[Piece]:
        """Get a piece by its name.
        
        Args:
            name: The name of the piece.
        
        Returns:
            The Piece instance if found, None otherwise.
        """
        return self._pieces.get(name)
    
    def get_all_pieces(self) -> List[Piece]:
        """Get all loaded pieces.
        
        Returns:
            List of all Piece instances.
        """
        return list(self._pieces.values())
    
    def get_piece_world_coordinates(self, piece_name: str, position_index: int, 
                                  variant_index: int) -> Optional[List[Tuple[float, float, float]]]:
        """Get the 3D world coordinates occupied by a piece in a specific position and variant.
        
        This is a stub implementation that will be expanded with the proper coordinate transformation
        system. For now, it returns None.
        
        Args:
            piece_name: The name of the piece.
            position_index: The integer index of the piece's origin position in the pyramid.
            variant_index: The variant index specifying the piece's transformation.
        
        Returns:
            List of (x, y, z) coordinates in world space, or None if piece not found.
        """
        piece = self.get_piece_by_name(piece_name)
        if piece is None:
            return None
            
        # Stub implementation - will be expanded with proper coordinate transformation
        return None
