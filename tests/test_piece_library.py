import json
import pytest
from iq_puzzler.piece_library import PieceLibrary


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

    return json_file


def test_piece_manager_initialization(sample_pieces_json):
    """Test that a PieceLibrary loads pieces correctly."""
    manager = PieceLibrary(sample_pieces_json)
    assert len(manager.pieces) == 2


def test_piece_variants(sample_pieces_json):
    """Test that pieces have valid variants computed."""
    manager = PieceLibrary(sample_pieces_json)

    # Each piece should have multiple valid rotations
    assert len(manager.pieces["Red Piece"]) > 1
    assert len(manager.pieces["Blue Piece"]) > 1


def test_unique_variants(sample_pieces_json):
    """Test that piece variants are unique (no duplicates after rotation)."""
    manager = PieceLibrary(sample_pieces_json)

    # For each piece, check that all its variants are unique
    for piece_name, variants in manager.pieces.items():
        # Convert positions to tuples for hashability
        variant_positions = [
            tuple(tuple(pos) for pos in variant.positions) for variant in variants
        ]
        # Convert to set and back to list to remove duplicates
        unique_positions = list(set(variant_positions))
        assert len(unique_positions) == len(variant_positions)
