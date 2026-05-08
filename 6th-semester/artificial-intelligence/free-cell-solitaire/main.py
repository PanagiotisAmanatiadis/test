"""Entry point for the FreeCell Solitaire solver."""

import argparse
import logging
import sys
from pathlib import Path

from freecell.algorithms import a_star_search, best_first_search, breadth_first_search, depth_first_search
from freecell.io import read_tableau, write_solution
from freecell.models import GameState

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

_ALGORITHMS = {
    "breadth": breadth_first_search,
    "depth":   depth_first_search,
    "best":    best_first_search,
    "astar":   a_star_search,
}

# Foundation sentinels — one per suit, initialised to rank 0 (empty).
_INITIAL_FOUNDATION = [["H0"], ["S0"], ["D0"], ["C0"]]
_INITIAL_FREE_CELLS: list[str | None] = [None, None, None, None]


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Solve a FreeCell Solitaire board using BFS, DFS, Best-First, or A*."
    )
    parser.add_argument(
        "algorithm",
        choices=list(_ALGORITHMS),
        help="Search algorithm to use.",
    )
    parser.add_argument("input_file",  type=Path, help="Path to the tableau input file.")
    parser.add_argument("output_file", type=Path, help="Path for the solution output file.")
    return parser


def main() -> None:
    """Parse arguments, initialise the game state, run the solver, and write results."""
    args = _build_arg_parser().parse_args()

    if not args.input_file.exists():
        logger.error("Input file not found: %s", args.input_file)
        sys.exit(1)

    tableau = read_tableau(args.input_file)
    import copy
    root = GameState(
        tableau=tableau,
        foundation=copy.deepcopy(_INITIAL_FOUNDATION),
        free_cells=list(_INITIAL_FREE_CELLS),
        parent=None,
    )

    algorithm = _ALGORITHMS[args.algorithm]
    moves, elapsed, solved = algorithm(root)

    if solved:
        write_solution(moves, elapsed, args.output_file)
    else:
        logger.warning("No solution found. Nodes explored: %d", len(moves))


if __name__ == "__main__":
    main()
