"""Backtracking solver for the IQ Puzzler game."""

from typing import List, Optional, Set
import logging
from .puzzle_state import PuzzleState
from .piece_library import PieceLibrary


class BacktrackingSolver:
    """Solves the IQ Puzzler game using backtracking search."""

    def __init__(self, state: PuzzleState, library: PieceLibrary):
        """Initialize the solver.

        Args:
            state: The initial puzzle state.
            library: Library containing all available pieces and their variants.
        """
        self.state = state
        self.library = library
        self.logger = logging.getLogger(__name__)

    def solve(self) -> Optional[PuzzleState]:
        """Find a solution using backtracking search.

        Returns:
            A solved puzzle state if a solution is found, None otherwise.
        """
        # Get all valid indices that need to be filled
        target_indices = set(self.state._model.get_all_indices())
        # Get all available pieces by name
        available_pieces = list(self.library.pieces.keys())

        self.logger.debug("Starting backtracking search")
        self.logger.debug(f"Target indices: {target_indices}")
        self.logger.debug(f"Available pieces: {available_pieces}")

        # Try to find a solution
        if self._solve_recursive(target_indices, available_pieces):
            self.logger.info("Solution found!")
            return self.state
        else:
            self.logger.info("No solution found")
            return None

    def _solve_recursive(
        self, remaining_indices: Set[int], available_pieces: List[str]
    ) -> bool:
        """Recursive helper for the backtracking search.

        Args:
            remaining_indices: Set of position indices that still need to be filled.
            available_pieces: List of piece names that are still available to use.

        Returns:
            True if a solution is found, False otherwise.
        """
        # Base case: if no indices remain, we found a solution
        if not remaining_indices:
            return True

        # Base case: if no pieces remain but indices do, no solution possible
        if not available_pieces:
            return False

        for index in sorted(remaining_indices):  # Sort for deterministic order
            self.logger.debug(
                f"{index}: Remaining number of pieces: {len(available_pieces)}"
            )
            for piece_name in available_pieces:
                for variant_idx, piece_variant in enumerate(
                    self.library.pieces[piece_name]
                ):
                    self.logger.debug(
                        f"Trying to place {piece_name} variant {variant_idx} at index {index} ({piece_variant.positions})"
                    )
                    # # Prompt user to continue
                    # user_input = input(
                    #     "Press Enter to continue, 'v' to skip variant, 'p' to skip piece: "
                    # ).lower()
                    # if user_input == "v":
                    #     continue
                    # elif user_input == "p":
                    #     break

                    if placement := self.state.place_piece(piece_variant, index):
                        self.logger.info(
                            f"Successfully placed {piece_name} variant {variant_idx} at index {index}"
                        )
                        # self.state.export_to_json(f"backtracking_{index}.json")

                        # Recursively try to solve the remaining puzzle
                        new_remaining_indices = (
                            remaining_indices - placement.occupied_indices
                        )
                        new_available_pieces = available_pieces.copy()
                        new_available_pieces.remove(piece_name)

                        if self._solve_recursive(
                            new_remaining_indices, new_available_pieces
                        ):
                            return True

                        # If no solution found, backtrack by removing the piece
                        self.state.remove_piece(piece_name)
                        self.logger.warning(
                            f"Backtracking: removed {piece_name} variant {variant_idx} from index {index}"
                        )

            self.logger.debug(f"No valid placement found for piece {piece_name}")

        # If we get here, no solution was found
        return False
