import pytest
from src.position_validator import PositionValidator

@pytest.fixture
def validator():
    """Create a PositionValidator instance for testing."""
    return PositionValidator()

def test_pyramid_structure(validator):
    """Test that the pyramid has the correct number of positions."""
    # Calculate expected positions:
    # Layer 0 (bottom): 4x4 = 16
    # Layer 1: 3x3 = 9
    # Layer 2: 2x2 = 4
    # Layer 3: 2x1 = 2
    # Layer 4 (top): 1x1 = 1
    # Total: 32 positions
    indices = validator.get_all_indices()
    assert len(indices) == 32
    assert min(indices) == 0
    assert max(indices) == 31

def test_valid_coordinates(validator):
    """Test conversion of valid coordinates to indices."""
    # Test some known positions
    # Bottom layer, corner positions
    assert validator.coord_to_index((0.0, 0.0, 0.0)) is not None
    assert validator.coord_to_index((3.0, 0.0, 0.0)) is not None
    assert validator.coord_to_index((0.0, 3.0, 0.0)) is not None
    assert validator.coord_to_index((3.0, 3.0, 0.0)) is not None
    
    # Top position
    assert validator.coord_to_index((1.5, 1.5, 4.0)) is not None

def test_invalid_coordinates(validator):
    """Test that invalid coordinates return None."""
    # Test positions outside the pyramid
    assert validator.coord_to_index((5.0, 0.0, 0.0)) is None  # Too far right
    assert validator.coord_to_index((0.0, 5.0, 0.0)) is None  # Too far back
    assert validator.coord_to_index((0.0, 0.0, 5.0)) is None  # Too high
    assert validator.coord_to_index((-1.0, 0.0, 0.0)) is None  # Negative coordinate

def test_coordinate_index_roundtrip(validator):
    """Test converting from coordinates to index and back."""
    # Test with a known valid position
    coord = (1.0, 1.0, 0.0)  # A position in the bottom layer
    index = validator.coord_to_index(coord)
    assert index is not None
    
    # Convert back to coordinates
    roundtrip_coord = validator.index_to_coord(index)
    assert roundtrip_coord is not None
    
    # Should get back the same coordinates (within floating point precision)
    assert all(abs(a - b) < 1e-6 for a, b in zip(coord, roundtrip_coord))

def test_invalid_index(validator):
    """Test that invalid indices return None."""
    # Test with an index that's too high
    assert validator.index_to_coord(999) is None
    assert not validator.is_valid_index(999)
    
    # Test with negative index
    assert validator.index_to_coord(-1) is None
    assert not validator.is_valid_index(-1)

def test_floating_point_precision(validator):
    """Test handling of floating-point imprecision."""
    # Test with slightly imprecise coordinates
    coord = (1.0000001, 1.0000001, 0.0000001)
    index = validator.coord_to_index(coord)
    
    # Should match the position (1.0, 1.0, 0.0)
    assert index is not None
    exact_coord = validator.index_to_coord(index)
    assert exact_coord == (1.0, 1.0, 0.0)

def test_layer_positions(validator):
    """Test positions in each layer of the pyramid."""
    # Bottom layer (z=0) should have 16 positions
    bottom_positions = [
        index for index in validator.get_all_indices()
        if validator.index_to_coord(index)[2] == 0.0
    ]
    assert len(bottom_positions) == 16
    
    # Top layer (z=4) should have 1 position
    top_positions = [
        index for index in validator.get_all_indices()
        if validator.index_to_coord(index)[2] == 4.0
    ]
    assert len(top_positions) == 1
