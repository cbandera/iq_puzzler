import pytest
import numpy as np
from src.piece import Piece2D
from src.piece3d import Piece3D


@pytest.fixture
def simple_piece2d():
    """Create a simple L-shaped 2D piece for testing."""
    return Piece2D(
        name="L Piece", color="rgb(255, 0, 0)", shape=[(0, 0), (1, 0), (0, 1)]
    )


def test_piece3d_initialization(simple_piece2d):
    """Test basic initialization of a Piece3D from a Piece2D."""
    piece3d = Piece3D(simple_piece2d)

    assert piece3d.name == "L Piece"
    assert piece3d.color == "rgb(255, 0, 0)"
    assert len(piece3d.get_variant_indices()) == 1  # Only base variant initially

    # Check base variant (original shape with z=0)
    base_variant = piece3d.get_variant(0)
    assert isinstance(base_variant, np.ndarray)
    assert base_variant.shape == (3, 3)  # 3 points, 3 coordinates each
    assert np.array_equal(base_variant[0], [0, 0, 0])
    assert np.array_equal(base_variant[1], [1, 0, 0])
    assert np.array_equal(base_variant[2], [0, 1, 0])


def test_piece3d_variant_management(simple_piece2d):
    """Test setting and getting variants."""
    piece3d = Piece3D(simple_piece2d)

    # Create some test variants
    variants = {
        0: np.array([(0, 0, 0), (1, 0, 0), (0, 1, 0)]),  # Original
        1: np.array([(0, 0, 0), (0, 1, 0), (0, 0, 1)]),  # Rotated
        2: np.array([(0, 0, 0), (-1, 0, 0), (0, -1, 0)]),  # Flipped
    }

    piece3d.set_variants(variants)

    # Check variant indices
    assert sorted(piece3d.get_variant_indices()) == [0, 1, 2]

    # Check each variant
    for idx, expected in variants.items():
        variant = piece3d.get_variant(idx)
        assert np.array_equal(variant, expected)


def test_piece3d_invalid_variant(simple_piece2d):
    """Test that accessing an invalid variant raises KeyError."""
    piece3d = Piece3D(simple_piece2d)

    with pytest.raises(KeyError):
        piece3d.get_variant(999)  # Non-existent variant


def test_piece3d_variant_copy(simple_piece2d):
    """Test that get_variant returns a copy of the variant."""
    piece3d = Piece3D(simple_piece2d)

    # Get the base variant and try to modify it
    variant = piece3d.get_variant(0)
    variant[0] = [99, 99, 99]

    # Original variant should be unchanged
    base_variant = piece3d.get_variant(0)
    assert not np.array_equal(base_variant[0], [99, 99, 99])
