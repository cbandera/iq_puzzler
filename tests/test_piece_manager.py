import json
import pytest
from src.piece_manager import PieceManager


@pytest.fixture
def sample_pieces_json(tmp_path):
    """Create a temporary JSON file with sample piece data."""
    pieces_data = [
        {
            "name": "Red Piece",
            "color": "rgb(255, 0, 0)",
            "grid": [
                True,
                True,
                False,
                False,
                True,
                False,
                False,
                False,
                False,
                False,
                False,
                False,
                False,
                False,
                False,
                False,
            ],
        },
        {
            "name": "Blue Piece",
            "color": "rgb(0, 0, 255)",
            "grid": [
                True,
                False,
                False,
                False,
                True,
                True,
                False,
                False,
                False,
                False,
                False,
                False,
                False,
                False,
                False,
                False,
            ],
        },
    ]

    json_file = tmp_path / "test_pieces.json"
    with open(json_file, "w") as f:
        json.dump(pieces_data, f)

    return str(json_file)


def test_piece_manager_initialization():
    """Test that a new PieceManager starts empty and has rotation matrices."""
    manager = PieceManager()
    assert len(manager.get_all_pieces()) == 0
    assert len(manager._rotation_matrices) == 48  # 4 * 3 * 4 = 48 possible rotations


def test_load_pieces_from_json(sample_pieces_json):
    """Test loading pieces from a JSON file."""
    manager = PieceManager()
    manager.load_pieces_from_json(sample_pieces_json)

    pieces = manager.get_all_pieces()
    assert len(pieces) == 2

    # Test we can get pieces by their names
    red_piece = manager.get_piece_by_name("Red Piece")
    assert red_piece is not None
    assert red_piece.name == "Red Piece"

    blue_piece = manager.get_piece_by_name("Blue Piece")
    assert blue_piece is not None
    assert blue_piece.name == "Blue Piece"


def test_get_nonexistent_piece():
    """Test getting a piece with a name that doesn't exist."""
    manager = PieceManager()
    piece = manager.get_piece_by_name("Green Piece")
    assert piece is None


def test_piece_scaling(sample_pieces_json):
    """Test that piece coordinates are properly scaled."""
    manager = PieceManager()
    manager.load_pieces_from_json(sample_pieces_json, scale=2.0)

    red_piece = manager.get_piece_by_name("Red Piece")
    shape = red_piece.get_shape()

    # Original coordinates were (0,0), (1,0), (0,1), now should be scaled by 2
    assert (0, 0) in shape
    assert (2, 0) in shape
    assert (0, 2) in shape


def test_piece_variants(sample_pieces_json):
    """Test that pieces have valid variants computed."""
    manager = PieceManager()
    manager.load_pieces_from_json(sample_pieces_json)

    red_piece = manager.get_piece_by_name("Red Piece")
    variants = red_piece.get_variant_indices()

    # Should have multiple variants
    assert len(variants) > 1

    # Test that each variant has integer coordinates
    for idx in variants:
        variant_shape = red_piece.get_variant(idx)
        for x, y in variant_shape:
            assert isinstance(x, int)
            assert isinstance(y, int)


def test_unique_variants(sample_pieces_json):
    """Test that piece variants are unique (no duplicates after rotation)."""
    manager = PieceManager()
    manager.load_pieces_from_json(sample_pieces_json)

    red_piece = manager.get_piece_by_name("Red Piece")
    variants = [
        tuple(sorted(red_piece.get_variant(idx)))
        for idx in red_piece.get_variant_indices()
    ]

    # Convert to set to remove duplicates and compare length
    unique_variants = set(variants)
    assert len(unique_variants) == len(variants)


def test_get_piece_world_coordinates(sample_pieces_json):
    """Test the stub implementation of get_piece_world_coordinates."""
    manager = PieceManager()
    manager.load_pieces_from_json(sample_pieces_json)

    # Test with existing piece
    coords = manager.get_piece_world_coordinates("Red Piece", 0, 0)
    assert coords is None  # Stub implementation returns None

    # Test with non-existent piece
    coords = manager.get_piece_world_coordinates("Green Piece", 0, 0)
    assert coords is None
