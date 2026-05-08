"""Intercept-point calculation and base selection logic.

An interceptor missile travels in a straight line at constant speed
``u_a = 1 500 m/s`` from its launch base.  Given the pre-simulated trajectory
of the incoming missile, we scan each time step to find the earliest moment T
at which the interceptor — launched at T = 0 — could reach the missile's
position.

The feasibility condition is simply::

    u_a * T  >=  ||r(T) - base_pos||

The first discrete time step satisfying this condition yields the intercept
time, the required launch direction, and the intercept position in ENU space.
"""

from __future__ import annotations

import logging
from typing import Optional

import numpy as np

logger = logging.getLogger(__name__)

INTERCEPTOR_SPEED: float = 1_500.0  # constant speed of the interceptor [m/s]


def find_intercept(
    trajectory: list[np.ndarray],
    base_pos: np.ndarray,
    dt: float,
) -> Optional[tuple[float, np.ndarray, np.ndarray]]:
    """Find the earliest feasible intercept for a single base.

    Args:
        trajectory: Simulated missile ENU positions at steps 0, dt, 2dt, …
        base_pos:   ENU position of the candidate launch base.
        dt:         Simulation time step [s].

    Returns:
        ``(t_intercept, direction, intercept_pos)`` if an intercept is
        possible, or *None* otherwise.
        *direction* is the unit vector pointing from the base to the
        intercept point — the required launch direction.
    """
    for i, pos in enumerate(trajectory):
        t = i * dt
        if t < 1e-9:
            continue   # interceptor has zero travel time at t = 0

        diff = pos - base_pos
        dist = float(np.linalg.norm(diff))
        if dist < 1e-6:
            continue   # missile is essentially on top of the base

        if INTERCEPTOR_SPEED * t >= dist:
            direction = diff / dist
            return t, direction, pos

    return None


def select_best_base(
    trajectory: list[np.ndarray],
    bases: list[np.ndarray],
    dt: float,
) -> tuple[Optional[int], Optional[float], Optional[np.ndarray], Optional[np.ndarray]]:
    """Choose the base that achieves the earliest intercept.

    Evaluates :func:`find_intercept` for every base and returns the one with
    the smallest ``t_intercept``, giving the missile the least time to travel
    further into the guarded zone.

    Args:
        trajectory: Simulated missile ENU positions.
        bases:      ENU positions of all available bases.
        dt:         Simulation time step [s].

    Returns:
        ``(base_index, t_intercept, direction, intercept_pos)``.
        All four values are *None* when no intercept is geometrically possible.
    """
    best: Optional[tuple[int, float, np.ndarray, np.ndarray]] = None

    for idx, base in enumerate(bases):
        result = find_intercept(trajectory, base, dt)
        if result is None:
            logger.debug("Base %d: no intercept solution found.", idx + 1)
            continue

        t_int, direction, pos = result
        logger.debug("Base %d: intercept at t = %.2f s.", idx + 1, t_int)

        if best is None or t_int < best[1]:
            best = (idx, t_int, direction, pos)

    if best is None:
        return None, None, None, None
    return best
