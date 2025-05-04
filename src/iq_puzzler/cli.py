#!/usr/bin/env python3

import click
import logging
from pathlib import Path
from typing import Optional
import colorama
from colorama import init as init_colorama

from iq_puzzler.piece_library import PieceLibrary
from iq_puzzler.puzzle_state import PuzzleState
from iq_puzzler.pyramid_model import PyramidModel
from iq_puzzler.rectangle_model import RectangleModel
from iq_puzzler.diamonds_model import DiamondsModel

init_colorama()


class ColorStreamHandler(logging.StreamHandler):
    """A custom stream handler for logging that uses colors for different log levels."""

    def __init__(self, stream=None):
        super().__init__(stream)
        self.color_map = {
            logging.DEBUG: colorama.Fore.CYAN,
            logging.INFO: colorama.Fore.GREEN,
            logging.WARNING: colorama.Fore.YELLOW,
            logging.ERROR: colorama.Fore.RED,
            logging.CRITICAL: colorama.Fore.RED + colorama.Style.BRIGHT,
        }

    def format(self, record: logging.LogRecord):
        record.msg = (
            self.color_map[record.levelno] + str(record.msg) + colorama.Style.RESET_ALL
        )
        return super().format(record)


DATA_DIR = Path(__file__).parent.parent.parent / "data"


def setup_logging(verbose: bool):
    """Configure logging based on verbosity level."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[ColorStreamHandler()],
    )


# Use Colorama to support colored output on Windows


@click.command()
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose logging")
@click.option(
    "--initial", type=click.Path(exists=True), help="Initial puzzle state JSON file"
)
@click.option(
    "--library",
    "piece_library",
    type=click.Path(exists=True, path_type=Path),
    default=DATA_DIR / "piece_library.json",
    help="Piece library JSON file",
)
@click.option(
    "--mode",
    type=click.Choice(["pyramid", "rectangle", "diamonds"], case_sensitive=False),
    default="pyramid",
    help="Game mode determining the final shape",
)
@click.option(
    "--solver",
    type=click.Choice(["backtracking", "dlx"], case_sensitive=False),
    default="backtracking",
    help="Solver algorithm to use",
)
@click.option("--output", type=click.Path(), help="Output file path for the solution")
def main(
    verbose: bool,
    initial: Optional[str],
    piece_library: Path,
    mode: str,
    solver: str,
    output: Optional[str],
):
    """IQ Puzzler Pro solver CLI.

    This tool helps solve different configurations of the IQ Puzzler Pro game
    using various solving strategies.
    """
    # Setup logging
    setup_logging(verbose)
    logger = logging.getLogger(__name__)

    logger.info(f"Starting IQ Puzzler solver in {mode} mode using {solver} algorithm")

    if mode == "pyramid":
        puzzle_model = PyramidModel()
    elif mode == "rectangle":
        puzzle_model = RectangleModel()
    elif mode == "diamonds":
        puzzle_model = DiamondsModel()
    else:
        raise ValueError(f"Invalid mode: {mode}")
    # Load piece library
    piece_manager = PieceLibrary(piece_library, puzzle_model)
    logger.debug(f"Loaded {len(piece_manager.pieces)} pieces from library")
    for name, variants in piece_manager.pieces.items():
        logger.debug("%s: %d" % (name, len(variants)))
        for idx, variant in enumerate(variants):
            logger.debug("%s: Variant %d" % (name, idx))
            logger.debug(variant.positions)

    # Initialize puzzle state
    puzzle_state = PuzzleState(puzzle_model)

    # TODO: Implement solver selection and execution
    logger.info("Solving puzzle...")

    # Save solution if output path is provided
    if output:
        logger.info(f"Saving solution to {output}")
        puzzle_state.export_to_json(output)

    return


if __name__ == "__main__":
    main()
