"""Fast Marching Method (FMM) for 3-D unsigned and signed distance computation.

Algorithm overview
------------------
The FMM solves the Eikonal equation ``|∇T| = 1`` outward from an interface
(the zero level-set of a given SDF) using a priority-queue (min-heap) strategy:

1. **Initialise** — identify interface nodes (nodes whose sign differs from
   at least one face-adjacent neighbour) and seed the heap with their
   analytic |SDF| values.
2. **Propagate** — repeatedly extract the node with the smallest tentative
   distance, mark it as *known*, and update its six face-adjacent neighbours
   using the upwind Eikonal stencil (see :mod:`fmm3d.eikonal`).

Signed distances are recovered by two independent FMM passes (exterior and
interior) combined with the sign of the original analytic SDF.

References
----------
Sethian, J.A. (1996). A fast marching level set method for monotonically
advancing fronts. *Proc. Natl. Acad. Sci.*, 93(4), 1591-1595.
"""

from __future__ import annotations

import heapq
import logging
import math

import numpy as np

from fmm3d.image import solve_eikonal
from fmm3d.grid import Grid

logger = logging.getLogger(__name__)

# Node state flags
_FAR   = 0   # not yet reached by the wavefront
_TRIAL = 1   # in the narrow band (inside the heap)
_KNOWN = 2   # accepted; distance is final


def _min_known_neighbor(
    dist: np.ndarray,
    state: np.ndarray,
    i: int,
    j: int,
    k: int,
    axis: int,
    n: int,
) -> float:
    """Return the minimum accepted distance among the two neighbours along *axis*.

    Args:
        dist:  Current distance array.
        state: Current state array (FAR / TRIAL / KNOWN).
        i, j, k: Indices of the node being updated.
        axis:  0 → x-axis, 1 → y-axis, 2 → z-axis.
        n:     Grid size per axis.

    Returns:
        Minimum KNOWN neighbour distance, or ``math.inf`` if none exists.
    """
    best = math.inf
    for delta in (-1, 1):
        idx       = [i, j, k]
        idx[axis] += delta
        ni, nj, nk = idx
        if 0 <= ni < n and 0 <= nj < n and 0 <= nk < n:
            if state[ni, nj, nk] == _KNOWN:
                best = min(best, float(dist[ni, nj, nk]))
    return best


def _update_distance(
    dist: np.ndarray,
    state: np.ndarray,
    i: int,
    j: int,
    k: int,
    n: int,
    h: float,
) -> float:
    """Compute the Eikonal-based distance estimate for node ``(i, j, k)``.

    Collects the minimum KNOWN neighbour along each axis, filters out
    unreachable directions, sorts ascending, and calls
    :func:`~fmm3d.eikonal.solve_eikonal`.

    Args:
        dist, state: Current distance and state arrays.
        i, j, k:    Node indices.
        n:          Grid size per axis.
        h:          Grid spacing.

    Returns:
        Updated distance estimate.
    """
    raw  = [_min_known_neighbor(dist, state, i, j, k, ax, n) for ax in range(3)]
    vals = sorted(v for v in raw if v < math.inf)
    return solve_eikonal(vals, h)


# ── Public API ─────────────────────────────────────────────────────────────────

def compute_unsigned_distance(grid: Grid, sdf: np.ndarray) -> np.ndarray:
    """Compute unsigned distances from the interface via FMM.

    Interface nodes — those with at least one face-adjacent neighbour of
    opposite SDF sign — are seeded with ``|sdf|`` (the analytic distance).
    The FMM then propagates accurate distances to all remaining nodes.

    Args:
        grid: Regular 3-D grid describing the computational domain.
        sdf:  Analytic signed distance field, shape ``(N, N, N)``.

    Returns:
        Unsigned distance array, shape ``(N, N, N)``.
    """
    n     = grid.n
    h     = grid.h
    signs = np.sign(sdf)

    dist  = np.full((n, n, n), math.inf, dtype=float)
    state = np.zeros((n, n, n), dtype=np.int8)   # all FAR
    heap: list[tuple[float, int, int, int]] = []

    # ── Seed the heap with interface nodes ────────────────────────────────────
    n_iface = 0
    _face_offsets = ((-1,0,0),(1,0,0),(0,-1,0),(0,1,0),(0,0,-1),(0,0,1))

    for i in range(n):
        for j in range(n):
            for k in range(n):
                s_ijk = signs[i, j, k]
                on_iface = False
                for di, dj, dk in _face_offsets:
                    ni, nj, nk = i + di, j + dj, k + dk
                    if 0 <= ni < n and 0 <= nj < n and 0 <= nk < n:
                        if signs[ni, nj, nk] != s_ijk:
                            on_iface = True
                            break

                if on_iface:
                    d              = abs(float(sdf[i, j, k]))
                    dist[i, j, k]  = d
                    state[i, j, k] = _TRIAL
                    heapq.heappush(heap, (d, i, j, k))
                    n_iface       += 1

    logger.info(
        "FMM: %d interface nodes seeded  (grid %d³, h = %.5f)",
        n_iface, n, h,
    )

    # ── FMM propagation loop ──────────────────────────────────────────────────
    processed = 0
    while heap:
        d, i, j, k = heapq.heappop(heap)

        # Lazy deletion: skip if already finalised
        if state[i, j, k] == _KNOWN:
            continue
        state[i, j, k] = _KNOWN
        processed     += 1

        # Update the six face-adjacent neighbours
        for di, dj, dk in _face_offsets:
            ni, nj, nk = i + di, j + dj, k + dk
            if not (0 <= ni < n and 0 <= nj < n and 0 <= nk < n):
                continue
            if state[ni, nj, nk] == _KNOWN:
                continue

            new_d = _update_distance(dist, state, ni, nj, nk, n, h)
            if new_d < dist[ni, nj, nk]:
                dist[ni, nj, nk]  = new_d
                state[ni, nj, nk] = _TRIAL
                heapq.heappush(heap, (new_d, ni, nj, nk))

    logger.info("FMM: %d / %d nodes finalised.", processed, n ** 3)
    return dist


def compute_signed_distance(grid: Grid, sdf: np.ndarray) -> np.ndarray:
    """Compute the full signed distance field using two FMM passes.

    Runs :func:`compute_unsigned_distance` once on the combined grid, then
    restores the sign from the original analytic *sdf*.

    Args:
        grid: Regular 3-D grid.
        sdf:  Analytic SDF array, shape ``(N, N, N)``.

    Returns:
        Signed distance array, shape ``(N, N, N)``.
    """
    logger.info("Computing signed distance field …")
    unsigned = compute_unsigned_distance(grid, sdf)
    # Interior nodes (sdf < 0) receive a negative distance
    return np.where(sdf >= 0.0, unsigned, -unsigned)
