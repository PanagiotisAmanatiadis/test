"""Search algorithms for FreeCell: BFS, DFS, Best-First, and A*."""

import logging
import time

from freecell.models import GameState

logger = logging.getLogger(__name__)

_TIME_LIMIT_SECONDS = 300  # 5 minutes


def _already_visited(visited: set[str], node: GameState) -> bool:
    return node.value_to_str() in visited


def breadth_first_search(root: GameState) -> tuple[list[str], float, bool]:
    """Solve using Breadth-First Search (time limit: 5 min).

    Args:
        root: Initial game state.

    Returns:
        3-tuple of (moves_explored, elapsed_seconds, solved).
    """
    logger.info("BFS started.")
    start = time.monotonic()
    queue: list[GameState] = [root]
    visited: set[str] = {root.value_to_str()}
    moves_explored: list[str] = [root.move]

    while queue and (elapsed := time.monotonic() - start) < _TIME_LIMIT_SECONDS:
        node = queue.pop(0)

        if node.check_if_win():
            elapsed = time.monotonic() - start
            logger.info("BFS solved in %.2f s (%d nodes).", elapsed, len(moves_explored))
            return moves_explored, elapsed, True

        all_moves = node.expand()
        for idx, child in enumerate(node.children):
            if not _already_visited(visited, child):
                queue.append(child)
                visited.add(child.value_to_str())
                child.move = all_moves[idx]
                moves_explored.append(child.move)

    elapsed = time.monotonic() - start
    logger.warning("BFS failed within %d s (%d nodes explored).", _TIME_LIMIT_SECONDS, len(moves_explored))
    return moves_explored, elapsed, False


def depth_first_search(root: GameState) -> tuple[list[str], float, bool]:
    """Solve using Depth-First Search (time limit: 5 min).

    Args:
        root: Initial game state.

    Returns:
        3-tuple of (moves_explored, elapsed_seconds, solved).
    """
    logger.info("DFS started.")
    start = time.monotonic()
    stack: list[GameState] = [root]
    visited: set[str] = {root.value_to_str()}
    moves_explored: list[str] = [root.move]

    while stack and (elapsed := time.monotonic() - start) < _TIME_LIMIT_SECONDS:
        node = stack.pop(0)

        if node.check_if_win():
            elapsed = time.monotonic() - start
            logger.info("DFS solved in %.2f s (%d nodes).", elapsed, len(moves_explored))
            return moves_explored, elapsed, True

        all_moves = node.expand()
        to_add: list[GameState] = []
        for idx, child in enumerate(node.children):
            if not _already_visited(visited, child):
                to_add.append(child)
                visited.add(child.value_to_str())
                child.move = all_moves[idx]
                moves_explored.append(child.move)

        to_add.reverse()
        stack[:0] = to_add

    elapsed = time.monotonic() - start
    logger.warning("DFS failed within %d s (%d nodes explored).", _TIME_LIMIT_SECONDS, len(moves_explored))
    return moves_explored, elapsed, False


def best_first_search(root: GameState) -> tuple[list[str], float, bool]:
    """Solve using Best-First Search (time limit: 5 min).

    Nodes are ordered by the greedy heuristic h(n) = cards not yet on foundation.

    Args:
        root: Initial game state.

    Returns:
        3-tuple of (moves_explored, elapsed_seconds, solved).
    """
    logger.info("Best-First Search started.")
    start = time.monotonic()
    frontier: list[GameState] = [root]
    visited: set[str] = {root.value_to_str()}
    moves_explored: list[str] = [root.move]

    while frontier and (elapsed := time.monotonic() - start) < _TIME_LIMIT_SECONDS:
        node = frontier.pop(0)

        if node.check_if_win():
            elapsed = time.monotonic() - start
            logger.info("Best-First solved in %.2f s (%d nodes).", elapsed, len(moves_explored))
            return moves_explored, elapsed, True

        all_moves = node.expand()
        for idx, child in enumerate(node.children):
            if not _already_visited(visited, child):
                frontier.append(child)
                visited.add(child.value_to_str())
                child.move = all_moves[idx]
                moves_explored.append(child.move)

        frontier.sort(key=lambda n: n.heuristic_score)

    elapsed = time.monotonic() - start
    logger.warning("Best-First failed within %d s (%d nodes explored).", _TIME_LIMIT_SECONDS, len(moves_explored))
    return moves_explored, elapsed, False


def a_star_search(root: GameState) -> tuple[list[str], float, bool]:
    """Solve using A* Search (time limit: 5 min).

    Nodes are ordered by f(n) = h(n) + g(n) where g(n) is the depth.

    Args:
        root: Initial game state.

    Returns:
        3-tuple of (moves_explored, elapsed_seconds, solved).
    """
    logger.info("A* Search started.")
    start = time.monotonic()
    frontier: list[GameState] = [root]
    visited: set[str] = {root.value_to_str()}
    moves_explored: list[str] = [root.move]

    while frontier and (elapsed := time.monotonic() - start) < _TIME_LIMIT_SECONDS:
        node = frontier.pop(0)

        if node.check_if_win():
            elapsed = time.monotonic() - start
            logger.info("A* solved in %.2f s (%d nodes).", elapsed, len(moves_explored))
            return moves_explored, elapsed, True

        all_moves = node.expand()
        for idx, child in enumerate(node.children):
            if not _already_visited(visited, child):
                frontier.append(child)
                visited.add(child.value_to_str())
                child.move = all_moves[idx]
                moves_explored.append(child.move)

        frontier.sort(key=lambda n: n.a_score)

    elapsed = time.monotonic() - start
    logger.warning("A* failed within %d s (%d nodes explored).", _TIME_LIMIT_SECONDS, len(moves_explored))
    return moves_explored, elapsed, False
