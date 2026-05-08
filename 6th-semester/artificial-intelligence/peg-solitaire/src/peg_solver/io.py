"""File I/O utilities for Peg Solitaire."""

import logging
from pathlib import Path

from peg_solver.models import Move

logger = logging.getLogger(__name__)


def read_board(path: Path) -> list[list[str]]:
    """Read a board file and return it as a 2-D list of strings.

    Each line in the file represents one row. Tokens are whitespace-separated,
    where '1' = peg and '2' = empty hole.

    Args:
        path: Path to the input board file.

    Returns:
        2-D list representing the board (row-major order).

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file is empty or malformed.
    """
    logger.info("Reading board from '%s'.", path)
    rows = [line.strip().split() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not rows:
        raise ValueError(f"Board file is empty: {path}")
    return rows


def write_solution(moves: list[Move], elapsed: float, path: Path) -> None:
    """Write the solution moves to an output file.

    Args:
        moves: Sequence of move dicts (each with keys 'x', 'y', "x'", "y'").
        elapsed: Total elapsed time in seconds.
        path: Destination file path (created or overwritten).
    """
    logger.info("Writing solution to '%s' (%d moves).", path, len(moves))
    elapsed_minutes = round(elapsed / 60, 2)
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"{len(moves)}\n")
        for move in moves:
            line = " ".join(str(v) for v in move.values())
            f.write(line + "\n")
    logger.info("Solution written (%.2f minutes elapsed).", elapsed_minutes)
