"""Search algorithms for Peg Solitaire: DFS and Best-First Search."""

import logging
import time

from peg_solver.models import Move, SearchNode

logger = logging.getLogger(__name__)

_TIME_LIMIT_SECONDS = 60


def depth_first_search(
    root: SearchNode,
) -> tuple[list[Move], float, bool]:
    """Solve the board using Depth-First Search (time limit: 60 s).

    Args:
        root: Initial board state as the root search node.

    Returns:
        A 3-tuple of (moves_explored, elapsed_seconds, solved).
        ``moves_explored`` contains the move dict of every node visited in
        exploration order; it is not guaranteed to be a direct solution path.
    """
    logger.info("DFS started.")
    start = time.monotonic()
    frontier: list[SearchNode] = [root]
    moves_explored: list[Move] = []

    while frontier and (elapsed := time.monotonic() - start) < _TIME_LIMIT_SECONDS:
        node = frontier.pop(0)
        moves_explored.append(node.move)

        if node.win():
            elapsed = time.monotonic() - start
            logger.info("DFS solved in %.2f s after %d nodes.", elapsed, len(moves_explored))
            return moves_explored, elapsed, True

        node.expand()
        children_reversed = list(reversed(node.children))
        frontier[:0] = children_reversed  # prepend to maintain DFS order

    elapsed = time.monotonic() - start
    logger.warning("DFS failed to solve within %d s (%d nodes explored).", _TIME_LIMIT_SECONDS, len(moves_explored))
    return moves_explored, elapsed, False


def best_first_search(
    root: SearchNode,
) -> tuple[list[Move], float, bool]:
    """Solve the board using Best-First Search (time limit: 60 s).

    The heuristic is the number of remaining pegs — fewer pegs is better.

    Args:
        root: Initial board state as the root search node.

    Returns:
        A 3-tuple of (moves_explored, elapsed_seconds, solved).
    """
    logger.info("Best-First Search started.")
    start = time.monotonic()
    frontier: list[SearchNode] = [root]
    moves_explored: list[Move] = []

    while frontier and (elapsed := time.monotonic() - start) < _TIME_LIMIT_SECONDS:
        node = frontier.pop(0)
        moves_explored.append(node.move)

        if node.win():
            elapsed = time.monotonic() - start
            logger.info("Best-First solved in %.2f s after %d nodes.", elapsed, len(moves_explored))
            return moves_explored, elapsed, True

        node.expand()
        frontier.extend(node.children)
        frontier.sort(key=lambda n: n.heuristic_score)

    elapsed = time.monotonic() - start
    logger.warning(
        "Best-First failed to solve within %d s (%d nodes explored).",
        _TIME_LIMIT_SECONDS, len(moves_explored),
    )
    return moves_explored, elapsed, False
