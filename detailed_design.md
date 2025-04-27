# Overview of Classes and Methods

This is a rough overview and will likely evolve.

**1. `PuzzleState` Class:**

* `__init__(initial_placement)`: Initializes the puzzle state based on the initial placement (converts initial (x, y, z) to integer indices and stores them).
* `place_piece(piece_color, position_index, orientation_index)`: Attempts to place a piece at the given location and orientation.
* `remove_piece(piece_color, position_index, orientation_index)`: Removes a placed piece.
* `is_solved()`: Checks if all pieces have been placed.
* `get_occupied_indices()`: Returns a set of currently occupied integer position indices.
* `get_placed_pieces()`: Returns a list of (piece\_color, position\_index, orientation\_index) tuples.

**2. `PlacementValidator` Class:**

* `is_valid_placement(piece_color, position_index, orientation_index, puzzle_state)`: Checks if the placement is valid (boundary, overlap, initial constraints).

**3. `Solver` (Interface):**

* `solve(initial_placement, pieces_to_place)`: Abstract method to find a solution.

**4. `BacktrackingSolver` Class (implements `Solver`):**

* `__init__(piece_manager, validator)`: Initializes the solver with a `PieceManager` and a `PlacementValidator`.
* `solve(initial_placement, pieces_to_place)`: Implements the backtracking algorithm. (Internal recursive helper methods will likely be needed).

**5. `PieceManager` Class:**

* `__init__()`: Initializes the piece shapes, valid orientations, and transformation data.
* `get_piece_shape(color)`: Returns the relative 2D coordinates for a given piece color.
* `get_valid_orientations(color)`: Returns a list of valid orientation indices for a given piece color.
* `get_occupied_indices_for_placement(color, position_index, orientation_index)`: Calculates the set of integer indices occupied by a piece given its color, a starting position index, and an orientation index.

**6. Input/Output Handler (CLI):**

* `parse_initial_placement()`: Reads and parses the initial placement from the CLI input.
* `display_solution(puzzle_state)`: Formats and prints the final solution to the CLI.
* `display_no_solution()`: Prints a message indicating that no solution was found.
