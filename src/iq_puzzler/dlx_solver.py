"""DLX solver for the IQ Puzzler game using Dancing Links algorithm."""

from __future__ import annotations
from typing import List, Optional, Set, Any
import logging
import time
from .puzzle_state import PuzzleState
from .piece_library import PieceLibrary
from . import coordinate_transformations


class DLXNode:
    """Node in the Dancing Links matrix.

    This is a specialized implementation of a circular doubly-linked list node
    that allows for efficient removal and restoration of nodes from the matrix.
    """

    def __init__(self, row: int, col: int):
        """Initialize a node.

        Args:
            row: Row index in the matrix.
            col: Column index in the matrix.
        """
        self.row = row
        self.col = col
        self.up: DLXNode = self
        self.down: DLXNode = self
        self.left: DLXNode = self
        self.right: DLXNode = self
        self.column_header: Optional[DLXColumnHeader] = None

    def remove_horizontal(self) -> None:
        """Remove this node from its horizontal linked list."""
        self.left.right = self.right
        self.right.left = self.left

    def restore_horizontal(self) -> None:
        """Restore this node to its horizontal linked list."""
        self.left.right = self
        self.right.left = self

    def remove_vertical(self) -> None:
        """Remove this node from its vertical linked list."""
        self.up.down = self.down
        self.down.up = self.up
        if self.column_header:
            self.column_header.size -= 1

    def restore_vertical(self) -> None:
        """Restore this node to its vertical linked list."""
        self.up.down = self
        self.down.up = self
        if self.column_header:
            self.column_header.size += 1


class DLXColumnHeader(DLXNode):
    """Column header node in the Dancing Links matrix."""

    def __init__(self, col: int, name: str):
        """Initialize a column header.

        Args:
            col: Column index in the matrix.
            name: Name of the column (for debugging).
        """
        super().__init__(-1, col)
        self.name = name
        self.size = 0  # Number of nodes in this column
        self.column_header = self


class DLXMatrix:
    """Dancing Links matrix for the exact cover problem."""

    def __init__(self, num_columns: int, column_names: List[str]):
        """Initialize the matrix.

        Args:
            num_columns: Number of columns in the matrix.
            column_names: Names of the columns.
        """
        # Create the root node
        self.root = DLXNode(-1, -1)

        # Create column headers
        self.column_headers: List[DLXColumnHeader] = []
        prev_header = self.root

        for col, name in enumerate(column_names):
            header = DLXColumnHeader(col, name)
            self.column_headers.append(header)

            # Link horizontally
            prev_header.right = header
            header.left = prev_header
            prev_header = header

        # Close the horizontal circular list
        prev_header.right = self.root
        self.root.left = prev_header

        # Row data for mapping back to puzzle pieces
        self.row_data: List[Any] = []

    def add_row(self, cols: List[int], row_data: Any) -> None:
        """Add a row to the matrix.

        Args:
            cols: List of column indices where this row has 1s.
            row_data: Data associated with this row (for solution reconstruction).
        """
        if not cols:
            return

        row = len(self.row_data)
        self.row_data.append(row_data)

        # Create nodes for this row
        prev_node = None
        first_node = None

        for col in cols:
            header = self.column_headers[col]
            node = DLXNode(row, col)
            node.column_header = header

            # Link vertically
            last_node_in_col = header.up
            last_node_in_col.down = node
            node.up = last_node_in_col
            node.down = header
            header.up = node
            header.size += 1

            # Link horizontally if not the first node
            if prev_node:
                prev_node.right = node
                node.left = prev_node
            else:
                first_node = node

            prev_node = node

        # Close the horizontal circular list
        if first_node and prev_node:
            prev_node.right = first_node
            first_node.left = prev_node

    def cover_column(self, col_header: DLXColumnHeader) -> None:
        """Cover a column in the matrix.

        This removes the column from the header list and removes all rows that have
        a 1 in this column from all other columns they have a 1 in.

        Args:
            col_header: The column header to cover.
        """
        # Remove the column header from the header list
        col_header.remove_horizontal()

        # Remove all rows that have a 1 in this column
        i = col_header.down
        while i != col_header:
            j = i.right
            while j != i:
                j.remove_vertical()
                j = j.right
            i = i.down

    def uncover_column(self, col_header: DLXColumnHeader) -> None:
        """Uncover a column in the matrix.

        This reverses the cover operation, restoring all rows and the column header.

        Args:
            col_header: The column header to uncover.
        """
        # Restore all rows that have a 1 in this column
        i = col_header.up
        while i != col_header:
            j = i.left
            while j != i:
                j.restore_vertical()
                j = j.left
            i = i.up

        # Restore the column header to the header list
        col_header.restore_horizontal()

    def choose_column(self) -> Optional[DLXColumnHeader]:
        """Choose the column with the fewest 1s (S heuristic).

        Returns:
            The column header with the minimum size.
        """
        min_size = float("inf")
        chosen_col = None

        j = self.root.right
        while j != self.root:
            if isinstance(j, DLXColumnHeader) and j.size < min_size:
                min_size = j.size
                chosen_col = j
            j = j.right

        return chosen_col


class DLXSolver:
    """Solves the IQ Puzzler game using Dancing Links algorithm (DLX)."""

    def __init__(self, state: PuzzleState, library: PieceLibrary):
        """Initialize the solver.

        Args:
            state: The initial puzzle state.
            library: Library containing all available pieces and their variants.
        """
        self.state = state
        self.library = library
        self.logger = logging.getLogger(__name__)
        self.solution: List[Any] = []
        self.matrix: Optional[DLXMatrix] = None
        self.debug_level = 3  # 0: none, 1: basic, 2: detailed, 3: verbose
        self.iterations = 0
        self.start_time = 0

    def _log_debug(self, level: int, message: str) -> None:
        """Log a debug message if the debug level is high enough.

        Args:
            level: Debug level of this message.
            message: The message to log.
        """
        if self.debug_level >= level:
            elapsed = time.time() - self.start_time
            self.logger.debug(f"[{elapsed:.2f}s] {message}")

    def solve(self) -> Optional[PuzzleState]:
        """Find a solution using DLX search.

        Returns:
            A solved puzzle state if a solution is found, None otherwise.
        """
        self.start_time = time.time()
        self.iterations = 0
        self.solution = []

        # Get all valid indices that need to be filled
        available_indices = (
            self.state.get_all_indices() - self.state.get_occupied_indices()
        )

        # Get all available pieces by name
        available_pieces = set(self.library.pieces.keys()) - set(
            self.state.get_placements().keys()
        )

        self.logger.info("Starting DLX search")
        self.logger.info(
            f"Available indices: {len(available_indices)} positions to fill"
        )
        self.logger.info(f"Available pieces: {len(available_pieces)} pieces to place")

        # Build the exact cover matrix
        self._build_matrix(available_indices, available_pieces)

        # Solve using Algorithm X
        if self._solve_dlx():
            self.logger.info(f"Solution found after {self.iterations} iterations!")
            self._apply_solution()
            return self.state
        else:
            self.logger.info(f"No solution found after {self.iterations} iterations")
            return None

    def _build_matrix(
        self, available_indices: Set[int], available_pieces: Set[str]
    ) -> None:
        """Build the exact cover matrix for the puzzle.

        The matrix has:
        - One column for each position in the pyramid (position constraint)
        - One column for each piece (piece constraint)
        - One row for each possible placement of each piece

        Args:
            available_indices: Set of position indices that need to be filled.
            available_pieces: Set of piece names that are available to use.
        """
        self._log_debug(1, "Building exact cover matrix...")

        # Create column names
        column_names = []

        # Position constraint columns (one for each position that needs to be filled)
        for idx in sorted(available_indices):
            column_names.append(f"pos_{idx}")

        # Piece constraint columns (one for each available piece)
        for piece_name in sorted(available_pieces):
            column_names.append(f"piece_{piece_name}")

        # Create the matrix
        self.matrix = DLXMatrix(len(column_names), column_names)

        # Map from column name to column index
        col_map = {name: i for i, name in enumerate(column_names)}

        # Add rows for each possible placement of each piece
        row_count = 0
        for piece_name in sorted(available_pieces):
            piece_variants = self.library.pieces[piece_name]
            self._log_debug(
                1, f"Processing piece {piece_name} with {len(piece_variants)} variants"
            )

            # For each variant of the piece
            for piece_variant in piece_variants:
                # For each possible starting position (only consider available positions)
                for position_idx in sorted(available_indices):
                    # Try to place the piece at this position
                    origin = self.state._model.index_to_coord(position_idx)
                    placed_piece = coordinate_transformations.translate(
                        piece_variant, origin
                    )

                    # Check if all positions are valid
                    if not all(
                        self.state._model.is_valid_coord(coord)
                        for coord in placed_piece.positions
                    ):
                        continue

                    # Get the indices occupied by this placement
                    occupied_indices = set()
                    valid_placement = True

                    for coord in placed_piece.positions:
                        idx = self.state._model.coord_to_index(coord)
                        if idx is None:
                            valid_placement = False
                            break
                        occupied_indices.add(idx)

                    if not valid_placement:
                        continue

                    # Skip if any position is not in the available indices
                    if not occupied_indices.issubset(available_indices):
                        continue

                    # Create a row for this placement
                    cols = []

                    # Add position constraints
                    for idx in occupied_indices:
                        cols.append(col_map[f"pos_{idx}"])

                    # Add piece constraint
                    cols.append(col_map[f"piece_{piece_name}"])

                    # Add the row to the matrix with placement data
                    placement_data = {
                        "piece_name": piece_name,
                        "start_idx": position_idx,
                        "occupied_indices": occupied_indices,
                        "piece": piece_variant,
                    }
                    self.matrix.add_row(cols, placement_data)
                    row_count += 1

        self._log_debug(
            1, f"Matrix built with {len(column_names)} columns and {row_count} rows"
        )

    def _solve_dlx(self) -> bool:
        """Solve the exact cover problem using Algorithm X with Dancing Links.

        Returns:
            True if a solution is found, False otherwise.
        """
        if not self.matrix:
            self.logger.error("Matrix not initialized")
            return False

        # Check if the matrix is empty (already solved)
        if self.matrix.root.right == self.matrix.root:
            return True

        self.iterations += 1
        if self.iterations % 10 == 0:
            self._log_debug(1, f"Iterations: {self.iterations}")

        # Choose a column to cover (S heuristic: column with fewest 1s)
        col = self.matrix.choose_column()
        if not col:
            return False

        self._log_debug(3, f"Choosing column {col.name} with {col.size} rows")

        # Cover the column
        self.matrix.cover_column(col)

        # Try each row in this column
        r = col.down
        while r != col:
            self._log_debug(3, f"Trying row {r.row}")

            # Add this row to the solution
            self.solution.append(self.matrix.row_data[r.row])

            # Cover all columns that have a 1 in this row
            j = r.right
            while j != r:
                self.matrix.cover_column(j.column_header)
                j = j.right

            # Recursively solve the reduced matrix
            if self._solve_dlx():
                return True

            # If no solution found, backtrack
            self._log_debug(3, f"Backtracking from row {r.row}")

            # Remove this row from the solution
            self.solution.pop()

            # Uncover all columns that have a 1 in this row (in reverse order)
            j = r.left
            while j != r:
                self.matrix.uncover_column(j.column_header)
                j = j.left

            r = r.down

        # Uncover the column we chose
        self.matrix.uncover_column(col)

        return False

    def _apply_solution(self) -> None:
        """Apply the found solution to the puzzle state."""
        self._log_debug(1, "Applying solution to puzzle state")

        for row_data in self.solution:
            piece_name = row_data["piece_name"]
            piece = row_data["piece"]
            position_idx = row_data["start_idx"]

            self._log_debug(2, f"Placing {piece_name} at index {position_idx}")

            # Place the piece in the puzzle state
            placement = self.state.place_piece(piece, position_idx)
            if not placement:
                self.logger.error(
                    f"Failed to place {piece_name} at index {position_idx}"
                )
