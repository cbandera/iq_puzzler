"""Tests for the PieceLibrary class."""

from iq_puzzler.piece_library import PieceLibrary


def test_piece_manager_initialization(mock_piece_library_json, mocked_model):
    """Test that a PieceLibrary loads pieces correctly."""
    manager = PieceLibrary(mock_piece_library_json, mocked_model)
    assert len(manager.pieces) == 2


def test_piece_variants(mock_piece_library_json, mocked_model, mock_piece):
    """Test that pieces have valid variants computed."""
    manager = PieceLibrary(mock_piece_library_json, mocked_model)

    # Use mock_piece for testing variants
    variants = manager._generate_variants(mock_piece)
    # Should have 8 unique rotations for this piece
    assert len(variants) == 8
    # Each variant should be unique
    positions_set = {tuple(map(tuple, v.positions)) for v in variants}
    assert len(positions_set) == 8


def test_unique_variants(mock_piece_library_json, mocked_model, mock_piece):
    """Test that piece variants are unique (no duplicates after rotation)."""
    manager = PieceLibrary(mock_piece_library_json, mocked_model)

    # Use mock_piece for testing variants
    variants = manager._generate_variants(mock_piece)
    # Convert each variant's positions to a hashable format
    variant_positions = [tuple(map(tuple, v.positions)) for v in variants]
    # Check that there are no duplicates
    assert len(variant_positions) == len(set(variant_positions))
