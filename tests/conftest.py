"""Common test fixtures."""

import json
import pytest

import numpy as np

from iq_puzzler.puzzle_piece import PuzzlePiece, Location3D
from iq_puzzler.puzzle_state import PuzzleState
from iq_puzzler.puzzle_model import PuzzleModel


class MockPuzzleModel(PuzzleModel):
    """Mock puzzle model for testing."""

    def __init__(self):
        """Initialize with a 3x3 grid at z=0."""
        self.valid_coords = {
            tuple(np.array([0.0, 0.0, 0.0])): 0,  # Origin
            tuple(np.array([1.0, 0.0, 0.0])): 1,  # Right
            tuple(np.array([2.0, 0.0, 0.0])): 2,  # Far right
            tuple(np.array([0.0, 1.0, 0.0])): 3,  # Up
            tuple(np.array([1.0, 1.0, 0.0])): 4,  # Up-right
            tuple(np.array([2.0, 1.0, 0.0])): 5,  # Up-far-right
            tuple(np.array([0.0, 2.0, 0.0])): 6,  # Far up
            tuple(np.array([1.0, 2.0, 0.0])): 7,  # Far up-right
            tuple(np.array([2.0, 2.0, 0.0])): 8,  # Far up-far-right
        }

    def coord_to_index(self, coord: Location3D) -> int | None:
        """Convert coordinates to index."""
        return self.valid_coords.get(tuple(coord))

    def index_to_coord(self, index: int) -> Location3D | None:
        """Convert index to coordinates."""
        for coord_tuple, idx in self.valid_coords.items():
            if idx == index:
                return np.array(coord_tuple)
        return None

    def is_valid_index(self, index: int) -> bool:
        """Check if index is valid."""
        return index in range(9)

    def is_valid_coord(self, coord: Location3D) -> bool:
        """Check if coordinates are valid."""
        return tuple(coord) in self.valid_coords

    def get_all_indices(self) -> list[int]:
        """Get all valid indices."""
        return list(range(9))

    def get_valid_rotations(self) -> list[tuple[float, float, float]]:
        """Get all valid rotation angle combinations."""
        return [
            (0, 0, 0),
            (90, 0, 0),
            (180, 0, 0),
            (270, 0, 0),
            (0, 0, 180),
            (90, 0, 180),
            (180, 0, 180),
            (270, 0, 180),
        ]


@pytest.fixture
def mocked_model():
    """Create a mock puzzle model."""
    return MockPuzzleModel()


@pytest.fixture
def mocked_state(mocked_model):
    """Create an empty puzzle state."""
    return PuzzleState(mocked_model)


@pytest.fixture
def mock_piece():
    """Create a test piece with a specific shape."""
    return PuzzlePiece(
        "Test",
        "rgb(255, 0, 0)",
        [
            Location3D(0, 0, 0),
            Location3D(1, 0, 0),
            Location3D(2, 0, 0),
            Location3D(2, 1, 0),
        ],
    )


@pytest.fixture
def pyramid():
    """Create a PyramidModel instance."""
    from iq_puzzler.pyramid_model import PyramidModel

    return PyramidModel()


@pytest.fixture
def mock_piece_library_json(tmp_path):
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
