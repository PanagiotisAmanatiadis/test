"""File I/O utilities for FreeCell Solitaire."""

import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def read_tableau(path: Path) -> list[list[str]]:
    """Read the initial tableau from a text file.

    Each line of the file represents one tableau stack. The last card on each
    line is the top card of the stack.

    Args:
        path: Path to the input file.

    Returns:
        List of piles (each pile is a list of card strings).

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file is empty.
    """
    logger.info("Reading tableau from '%s'.", path)
    lines = [line.strip().split() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not lines:
        raise ValueError(f"Input file is empty: {path}")
    return lines


def write_solution(moves: list[str], elapsed: float, path: Path) -> None:
    """Write explored moves and timing to an output file.

    Args:
        moves: Sequence of move description strings.
        elapsed: Total elapsed time in seconds.
        path: Destination file path (created or overwritten).
    """
    elapsed_minutes = round(elapsed / 60, 2)
    logger.info("Writing solution to '%s' (%d moves, %.2f min).", path, len(moves), elapsed_minutes)
    with open(path, "w", encoding="utf-8") as f:
        f.write(
            f"Total moves to win: {len(moves)}, "
            f"time: {elapsed_minutes} minutes\n"
        )
        for move in moves:
            f.write(move + "\n")
