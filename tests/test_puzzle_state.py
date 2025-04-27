import pytest
from src.puzzle_state import PuzzleState, PiecePlacement

@pytest.fixture
def empty_state():
    """Create an empty puzzle state."""
    return PuzzleState()

@pytest.fixture
def state_with_piece(empty_state):
    """Create a puzzle state with one piece placed."""
    empty_state.place_piece(
        color="rgb(255, 0, 0)",
        position_index=0,
        orientation_index=0,
        occupied_indices={0, 1, 2}
    )
    return empty_state

def test_initial_state(empty_state):
    """Test that a new puzzle state starts empty."""
    assert len(empty_state.get_placed_pieces()) == 0
    assert len(empty_state.get_occupied_indices()) == 0

def test_place_piece(empty_state):
    """Test placing a piece in an empty state."""
    success = empty_state.place_piece(
        color="rgb(255, 0, 0)",
        position_index=0,
        orientation_index=0,
        occupied_indices={0, 1, 2}
    )
    
    assert success
    assert empty_state.is_piece_placed("rgb(255, 0, 0)")
    assert empty_state.get_occupied_indices() == {0, 1, 2}
    
    placement = empty_state.get_placement("rgb(255, 0, 0)")
    assert placement is not None
    assert placement.color == "rgb(255, 0, 0)"
    assert placement.position_index == 0
    assert placement.orientation_index == 0
    assert placement.occupied_indices == {0, 1, 2}

def test_place_piece_overlap(state_with_piece):
    """Test that placing a piece that would overlap fails."""
    # Try to place a piece that would occupy some of the same indices
    success = state_with_piece.place_piece(
        color="rgb(0, 255, 0)",
        position_index=1,
        orientation_index=0,
        occupied_indices={2, 3, 4}  # Note: 2 overlaps with first piece
    )
    
    assert not success
    assert not state_with_piece.is_piece_placed("rgb(0, 255, 0)")
    assert state_with_piece.get_occupied_indices() == {0, 1, 2}  # Unchanged

def test_place_same_piece_twice(state_with_piece):
    """Test that placing the same piece twice fails."""
    success = state_with_piece.place_piece(
        color="rgb(255, 0, 0)",  # Same color as piece in state_with_piece
        position_index=5,
        orientation_index=1,
        occupied_indices={5, 6, 7}
    )
    
    assert not success
    placement = state_with_piece.get_placement("rgb(255, 0, 0)")
    assert placement.position_index == 0  # Original position unchanged

def test_remove_piece(state_with_piece):
    """Test removing a placed piece."""
    success = state_with_piece.remove_piece("rgb(255, 0, 0)")
    
    assert success
    assert not state_with_piece.is_piece_placed("rgb(255, 0, 0)")
    assert len(state_with_piece.get_occupied_indices()) == 0

def test_remove_nonexistent_piece(empty_state):
    """Test attempting to remove a piece that isn't placed."""
    success = empty_state.remove_piece("rgb(255, 0, 0)")
    assert not success

def test_get_placement_nonexistent(empty_state):
    """Test getting placement for a piece that isn't placed."""
    placement = empty_state.get_placement("rgb(255, 0, 0)")
    assert placement is None

def test_get_placed_pieces(state_with_piece):
    """Test getting list of all placed pieces."""
    pieces = state_with_piece.get_placed_pieces()
    assert len(pieces) == 1
    assert pieces[0].color == "rgb(255, 0, 0)"
    assert pieces[0].position_index == 0
    assert pieces[0].orientation_index == 0
    assert pieces[0].occupied_indices == {0, 1, 2}
