from src.piece import Piece2D


def test_piece2d_initialization():
    """Test basic initialization of a Piece2D."""
    name = "Test Piece"
    color = "rgb(255, 0, 0)"
    shape = [(0, 0), (1, 0), (0, 1)]

    piece = Piece2D(name, color, shape)

    assert piece.name == name
    assert piece.color == color
    assert piece.get_shape() == shape


def test_piece2d_shape_is_copied():
    """Test that get_shape returns a copy of the shape."""
    shape = [(0, 0), (1, 0)]
    piece = Piece2D("Test", "rgb(255, 0, 0)", shape)

    # Get the shape and modify it
    returned_shape = piece.get_shape()
    returned_shape.append((2, 0))

    # Original shape should be unchanged
    assert piece.get_shape() == [(0, 0), (1, 0)]


def test_piece2d_from_json_basic():
    """Test creating a Piece2D from JSON with default scaling."""
    json_data = {
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
    }

    piece = Piece2D.from_json(json_data)

    assert piece.name == "Red Piece"
    assert piece.color == "rgb(255, 0, 0)"
    # With default scaling (2.0), coordinates should be multiplied by 2
    expected_shape = [(0, 0), (2, 0), (0, 2)]
    assert sorted(piece.get_shape()) == sorted(expected_shape)


def test_piece2d_from_json_custom_scale():
    """Test creating a Piece2D from JSON with custom scaling."""
    json_data = {
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
    }

    piece = Piece2D.from_json(json_data, scale=3.0)

    # With scaling of 3.0, coordinates should be multiplied by 3
    expected_shape = [(0, 0), (0, 3), (3, 3)]
    assert sorted(piece.get_shape()) == sorted(expected_shape)
