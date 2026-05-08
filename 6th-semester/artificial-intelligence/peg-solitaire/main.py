"""Entry point for the Peg Solitaire solver."""

import argparse
import logging
import sys
from pathlib import Path

from peg_solver.algorithms import best_first_search, depth_first_search
from peg_solver.io import read_board, write_solution
from peg_solver.models import SearchNode

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

_ALGORITHMS = {
    "depth": depth_first_search,
    "best": best_first_search,
}


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Solve a Peg Solitaire board using DFS or Best-First Search."
    )
    parser.add_argument(
        "algorithm",
        choices=list(_ALGORITHMS),
        help="Search algorithm: 'depth' for DFS, 'best' for Best-First.",
    )
    parser.add_argument("input_file", type=Path, help="Path to the board input file.")
    parser.add_argument("output_file", type=Path, help="Path for the solution output file.")
    return parser


def main() -> None:
    """Parse arguments, load the board, run the solver, and write results."""
    args = _build_arg_parser().parse_args()

    if not args.input_file.exists():
        logger.error("Input file not found: %s", args.input_file)
        sys.exit(1)

    board = read_board(args.input_file)
    # First row is a header/metadata line in the assignment format; skip it.
    state = board[1:]
    root = SearchNode(state, parent=None)

    algorithm = _ALGORITHMS[args.algorithm]
    moves, elapsed, solved = algorithm(root)

    if solved:
        write_solution(moves, elapsed, args.output_file)
    else:
        logger.warning("No solution found. Nodes explored: %d", len(moves))


if __name__ == "__main__":
    main()
