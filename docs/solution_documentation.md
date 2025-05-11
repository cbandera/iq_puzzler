# Design and Solution Strategy

**1. Core Concepts:**

* **Indexed 3D Position:** A unique integer index is assigned to each valid ball position within the 5-layer pyramid. This index provides a simplified way to refer to locations and perform boundary checks.
* **Floating-Point 3D Coordinates:** Each integer position index maps to a corresponding (x, y, z) floating-point coordinate in 3D space, accurately representing the shifted layers. These coordinates are primarily for visualization and detailed consistency checks.
* **Piece Variant:** Each piece can be transformed into multiple valid variants through rotation. A variant is considered valid only if all resulting coordinates after transformation are integers. Each valid variant is associated with an integer index.
* **Piece Shape:** The shape of each puzzle piece is defined as a set of 2D relative coordinates in its local xy-plane, starting from an "origin" ball. These coordinates are scaled by a factor of 2 to ensure proper spacing.
* **Placement:** A placement of a piece is defined by the integer index of one of its balls (the "origin") and a variant index.
* **Coordinate Transformation:** For a given piece, position index, and variant index, a transformation process using precomputed rotation matrices converts the piece's local 2D coordinates into the 3D world coordinates (and the corresponding integer indices) it occupies.
* **Puzzle State:** Represents the current configuration of placed pieces, including their names, position indices, and variant indices.

**2. Architecture:**

The application will be structured with the following core components:

* **`PuzzleState`:**
    * **Responsibility:** Manages the current state of the puzzle, including which pieces are placed and their placements (piece name, position index, variant index).
    * **Interfaces:**
        * Provides methods to place a piece, remove a piece, check if all pieces are placed, retrieve the set of occupied integer indices, and access the list of placed pieces.
* **`PlacementValidator`:**
    * **Responsibility:** Determines if a proposed placement of a piece is valid given the current puzzle state and any initial constraints.
    * **Interfaces:**
        * A method `is_valid_placement(piece_name, position_index, variant_index, puzzle_state)` that returns a boolean indicating the validity of the placement. This will involve boundary checks (using integer indices), overlap checks (against occupied integer indices), and adherence to initial placement constraints (matching piece name to the initially specified position).
* **`Solver` (Interface):**
    * **Responsibility:** Defines the contract for any algorithm that attempts to find a solution to the puzzle.
    * **Interfaces:**
        * A method `solve(initial_placement, pieces_to_place)` that takes the initial placement and the list of remaining pieces and returns a `PuzzleState` representing the solution or `None`.
* **`BacktrackingSolver` (Implementation of `Solver`):**
    * **Responsibility:** Implements a backtracking algorithm to search for a valid solution. It will use the `PuzzleState` to track the current state and the `PlacementValidator` to check the validity of potential placements.
    * **Interfaces:**
        * Implements the `solve` method defined in the `Solver` interface.
* **`PieceManager`:**
    * **Responsibility:** Stores and provides access to the shapes of all the puzzle pieces (mapping name to the set of relative 2D coordinates). It will also be responsible for managing the precomputed valid variants and the associated coordinate transformations for each piece.
    * **Interfaces:**
        * Methods to get the shape of a piece by its name.
        * Methods to get the set of valid variant indices for a piece.
        * Methods to get the 3D world coordinates (and integer indices) occupied by a piece given its name, position index, and variant index.
        * Methods to load piece definitions from a JSON file at startup, applying a scaling factor of 2 to coordinates.
    * **Rotation System:**
        * 24 rotation matrices are precomputed at startup, representing all possible combinations of:
            * Z-axis rotations (0°, 90°, 180°, 270°)
            * Y-axis rotations (0°, ±45°)
            * X-axis rotations (0°, ±90°, 180°)
        * Each piece's valid variants are determined by:
            1. Applying each rotation matrix to the piece's coordinates
            2. Checking if all resulting coordinates are integers
            3. Storing only the valid transformations as variants
        * Each valid variant is assigned a unique index for efficient lookup
* **Input/Output Handler (CLI):**
    * **Responsibility:** Handles the input from the CLI (initial placement) and outputs the final solution or indicates if no solution is found.
    * **Interfaces:**
        * Methods to parse the initial placement from the user input.
        * Methods to format and display the final solution (piece names and their placements).
