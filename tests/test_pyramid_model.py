"""Tests for the PyramidModel class."""

from iq_puzzler.coordinates import Location3D, XY_DIST, Z_DIST
from iq_puzzler.coordinate_transformations import (
    is_rotation_matrix_orthogonal,
    rotation_matrix,
    rotate,
    align_with_grid_positions,
)
import numpy as np


def test_pyramid_structure_initialization(pyramid):
    """Test that the pyramid structure is correctly initialized."""
    # Test basic properties
    assert len(pyramid.get_all_indices()) == 55  # 25 + 16 + 9 + 4 + 1 = 55 positions

    # Test some specific coordinates
    # Bottom layer (5x5)
    assert pyramid.coord_to_index(Location3D(0.0, 0.0, 0.0)) == 0  # Bottom left corner
    assert (
        pyramid.coord_to_index(Location3D(4.0 * XY_DIST, 0.0, 0.0)) == 4
    )  # Bottom right corner
    assert (
        pyramid.coord_to_index(Location3D(0.0, 4.0 * XY_DIST, 0.0)) == 20
    )  # Top left corner
    assert (
        pyramid.coord_to_index(Location3D(4.0 * XY_DIST, 4.0 * XY_DIST, 0.0)) == 24
    )  # Top right corner

    # Second layer (4x4)
    assert (
        pyramid.coord_to_index(Location3D(0.5 * XY_DIST, 0.5 * XY_DIST, Z_DIST))
        is not None
    )

    # Third layer (3x3)
    assert (
        pyramid.coord_to_index(Location3D(XY_DIST, XY_DIST, 2 * Z_DIST)) is not None
    )  # First position in third layer

    # Top layer (1x1)
    assert (
        pyramid.coord_to_index(Location3D(2.0 * XY_DIST, 2.0 * XY_DIST, 4 * Z_DIST))
        is not None
    )  # Top position


def test_coord_to_index_conversion(pyramid):
    """Test coordinate to index conversion."""
    # Test valid coordinates
    assert pyramid.coord_to_index(Location3D(0.0, 0.0, 0.0)) == 0

    # Test invalid coordinates
    assert pyramid.coord_to_index(Location3D(-1.0, 0.0, 0.0)) is None
    assert (
        pyramid.coord_to_index(Location3D(0.0, 0.0, Z_DIST)) is None
    )  # Invalid z-level

    # Test floating point precision handling
    assert pyramid.coord_to_index(Location3D(0.0000001, 0.0, 0.0)) == 0
    assert pyramid.coord_to_index(Location3D(0.0, 0.0000001, 0.0)) == 0


def test_index_to_coord_conversion(pyramid):
    """Test index to coordinate conversion."""
    # Test valid indices
    assert pyramid.index_to_coord(0) == Location3D(0.0, 0.0, 0.0)

    # Test invalid indices
    assert pyramid.index_to_coord(-1) is None
    assert pyramid.index_to_coord(55) is None  # Out of range

    # Test roundtrip conversion
    coord = Location3D(
        XY_DIST, XY_DIST, 2 * Z_DIST
    )  # A valid coordinate in the third layer
    index = pyramid.coord_to_index(coord)
    assert index is not None
    assert pyramid.index_to_coord(index) == coord


def test_validation_methods(pyramid):
    """Test validation methods for indices and coordinates."""
    # Test valid cases
    assert pyramid.is_valid_index(0)
    assert pyramid.is_valid_index(54)
    assert pyramid.is_valid_coord(Location3D(0.0, 0.0, 0.0))
    assert pyramid.is_valid_coord(
        Location3D(2.0 * XY_DIST, 2.0 * XY_DIST, 4 * Z_DIST)
    )  # Top position

    # Test invalid cases
    assert not pyramid.is_valid_index(-1)
    assert not pyramid.is_valid_index(55)
    assert not pyramid.is_valid_coord(Location3D(-1.0, 0.0, 0.0))
    assert not pyramid.is_valid_coord(Location3D(0.0, 0.0, 5 * Z_DIST))  # Above top

    # Test edge cases with floating point precision
    assert pyramid.is_valid_coord(Location3D(0.0000001, 0.0, 0.0))


def test_layer_structure(pyramid):
    """Test the structure of each layer in the pyramid."""
    # Layer 0 (bottom, 5x5)
    bottom_layer = {
        coord for coord, idx in pyramid._coord_to_index.items() if coord.z == 0.0
    }
    assert len(bottom_layer) == 25

    # Layer 1 (4x4)
    layer_1 = {
        coord for coord, idx in pyramid._coord_to_index.items() if coord.z == Z_DIST
    }
    assert len(layer_1) == 16

    # Layer 2 (3x3)
    layer_2 = {
        coord for coord, idx in pyramid._coord_to_index.items() if coord.z == 2 * Z_DIST
    }
    assert len(layer_2) == 9

    # Layer 3 (2x2)
    layer_3 = {
        coord for coord, idx in pyramid._coord_to_index.items() if coord.z == 3 * Z_DIST
    }
    assert len(layer_3) == 4

    # Layer 4 (top, 1x1)
    layer_4 = {
        coord for coord, idx in pyramid._coord_to_index.items() if coord.z == 4 * Z_DIST
    }
    assert len(layer_4) == 1


def test_valid_rotations(pyramid):
    """Test that all valid rotations produce orthogonal rotation matrices."""
    valid_rotations = pyramid.get_valid_rotations()
    # PyramidModel should have exactly 24 valid rotations
    assert len(valid_rotations) == 24

    # Each rotation should produce a valid orthogonal rotation matrix
    for yaw, pitch, roll in valid_rotations:
        r_matrix = rotation_matrix(yaw, pitch, roll)
        assert is_rotation_matrix_orthogonal(r_matrix), (
            f"Rotation matrix for angles (yaw={yaw}, pitch={pitch}, roll={roll}) "
            "is not a proper orthogonal matrix"
        )


def test_piece_rotations(pyramid, mock_piece):
    """Test that all valid rotations of a piece result in grid-aligned pieces."""
    valid_rotations = pyramid.get_valid_rotations()
    assert len(valid_rotations) == 24

    # Each rotation should produce a valid piece with grid-aligned positions
    for yaw, pitch, roll in valid_rotations:
        r_matrix = rotation_matrix(yaw, pitch, roll)
        rotated_piece = rotate(mock_piece, r_matrix)
        assert rotated_piece is not None, (
            f"Rotation failed for angles (yaw={yaw}, pitch={pitch}, roll={roll})"
        )

        # The rotated piece should already be grid-aligned
        # Trying to align it again should not change the positions
        aligned_positions = align_with_grid_positions(rotated_piece.positions)
        np.testing.assert_allclose(
            aligned_positions,
            rotated_piece.positions,
            atol=1e-10,
            err_msg=(
                f"Rotated piece positions for angles (yaw={yaw}, pitch={pitch}, "
                f"roll={roll}) are not grid-aligned"
            ),
        )
