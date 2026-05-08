"""Upwind finite-difference solver for the 3-D Eikonal equation.

The Eikonal equation ``|∇T| = 1`` on a regular grid with spacing *h* is
discretised using the standard upwind stencil.  Given the minimum known
neighbour distances ``a ≤ b ≤ c`` in the three coordinate directions, the
update formula for a node T is:

    1-D  (only x-neighbour known):    T = a + h
    2-D  (x and y known):             T = (a + b + √(2h² - (b-a)²)) / 2
    3-D  (all three known):           T = (a + b + c + √((a+b+c)² - 3(a²+b²+c²-h²))) / 3

Each case is tried in turn; the smallest valid result is returned.
"""

import math


def solve_eikonal(neighbors: list[float], h: float) -> float:
    """Solve the upwind Eikonal equation for one grid node.

    *neighbors* must contain only finite (already accepted) values from the
    three axis directions, sorted in ascending order.  Missing directions are
    simply omitted.

    Args:
        neighbors: Sorted list of 1–3 known neighbour distances (all finite).
        h:         Grid spacing.

    Returns:
        Updated distance estimate for the node.
    """
    n = len(neighbors)
    if n == 0:
        return math.inf

    a = neighbors[0]

    # ── Case 1: 1-D update from the closest neighbour ────────────────────────
    t1 = a + h
    if n == 1 or t1 <= neighbors[1]:
        return t1

    # ── Case 2: 2-D update using the two closest neighbours ─────────────────
    b     = neighbors[1]
    disc2 = 2.0 * h * h - (b - a) ** 2
    if disc2 >= 0.0:
        t2 = (a + b + math.sqrt(disc2)) / 2.0
        if n == 2 or t2 <= neighbors[2]:
            return t2

    if n == 2:
        return b + h   # 1-D fallback from the second neighbour

    # ── Case 3: 3-D update using all three neighbours ────────────────────────
    c     = neighbors[2]
    s     = a + b + c
    disc3 = s * s - 3.0 * (a * a + b * b + c * c - h * h)
    if disc3 >= 0.0:
        return (s + math.sqrt(disc3)) / 3.0

    # Fallback: degenerate geometry — use the best available lower-order result
    if disc2 >= 0.0:
        return (a + b + math.sqrt(disc2)) / 2.0
    return b + h
