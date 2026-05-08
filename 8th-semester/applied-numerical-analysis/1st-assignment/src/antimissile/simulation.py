"""Main simulation loop for the Thessaloniki anti-missile defence system.

Workflow
--------
1. A random incoming missile is generated at the radar detection boundary
   (30 km from the radar station).
2. Its full trajectory is predicted by integrating the missile ODE (RK4,
   dt = 0.1 s) until ground impact.
3. All three anti-missile bases evaluate whether they can intercept the
   missile; the base with the earliest intercept time is selected.
4. All events are reported via structured logging in chronological order.
"""

from __future__ import annotations

import logging

import numpy as np

from antimissile.coordinates import geo_to_enu, RADAR_GEO, GROUND_Z_ENU
from antimissile.physics import rk4_step
from antimissile.intercept import select_best_base, INTERCEPTOR_SPEED

logger = logging.getLogger(__name__)

# ── Simulation constants ───────────────────────────────────────────────────────
DT           = 0.1       # time step [s]
RADAR_RANGE  = 30_000.0  # radar detection range [m]
MAX_SIM_TIME = 7_200.0   # safety cap on simulation duration [s]

# Anti-missile base geodetic positions (lat °, lon °, elev m ASL)
_BASES_GEO = [
    (40.7623502, 23.0628008, 107.8),   # Base 1
    (40.6350068, 23.3369694, 478.6),   # Base 2
    (40.5835746, 22.9887777, 96.5),    # Base 3
]
BASES: list[np.ndarray] = [geo_to_enu(*b) for b in _BASES_GEO]

# Radar ENU position is the frame origin
RADAR_ENU = np.zeros(3)


def _generate_missile(rng: np.random.Generator) -> tuple[np.ndarray, np.ndarray]:
    """Generate a random incoming missile entering the radar coverage sphere.

    The missile entry point is placed on the 30 km detection sphere at a
    positive ENU altitude.  Its velocity is biased toward the guarded area
    and has a downward (descending) component.

    Args:
        rng: NumPy random Generator for reproducible missile generation.

    Returns:
        ``(r0, v0)`` — initial ENU position [m] and velocity [m/s].
    """
    while True:
        # Random entry direction with guaranteed positive altitude
        raw     = rng.standard_normal(3)
        raw[2]  = abs(raw[2]) + 0.3    # ensure the entry point is above radar
        entry   = raw / np.linalg.norm(raw)
        r0      = entry * RADAR_RANGE  # position on the detection sphere [m]

        # Velocity: aimed roughly toward the centre of the guarded area
        speed   = rng.uniform(1_000.0, 1_500.0)
        toward  = -entry + rng.standard_normal(3) * 0.25
        toward[2] -= 0.4               # additional downward bias
        toward  /= np.linalg.norm(toward)
        v0      = speed * toward

        if v0[2] < 0.0:                # accept only descending trajectories
            return r0, v0


class Simulation:
    """Discrete-time anti-missile simulation for Thessaloniki.

    Args:
        seed: Integer seed passed to ``numpy.random.default_rng`` for
              reproducible missile generation.
    """

    def __init__(self, seed: int = 42) -> None:
        self._rng = np.random.default_rng(seed)

    def run(self, n_missiles: int = 1) -> None:
        """Simulate *n_missiles* independent incoming missile events.

        Args:
            n_missiles: Number of missiles to generate and attempt to intercept.
        """
        for mid in range(1, n_missiles + 1):
            self._simulate_one(mid)

    # ── private helpers ────────────────────────────────────────────────────────

    def _simulate_one(self, missile_id: int) -> None:
        """Run the full detection-to-intercept sequence for one missile."""
        r0, v0 = _generate_missile(self._rng)
        state  = np.concatenate([r0, v0])

        logger.info("=" * 65)
        logger.info("t = 0.0 s | MISSILE #%d — RADAR DETECTION", missile_id)
        logger.info("  Entry position (ENU m) : [%8.0f, %8.0f, %8.0f]", *r0)
        logger.info("  Speed                  : %.0f m/s", float(np.linalg.norm(v0)))
        logger.info("  Velocity   (ENU m/s)   : [%7.1f, %7.1f, %7.1f]", *v0)

        # ── Step 1: predict full trajectory by RK4 integration ────────────────
        trajectory: list[np.ndarray] = []
        s = state.copy()
        t_sim = 0.0

        while s[2] > GROUND_Z_ENU and t_sim <= MAX_SIM_TIME:
            trajectory.append(s[:3].copy())
            s     = rk4_step(s, DT)
            t_sim += DT

        if len(trajectory) < 2:
            logger.warning("  MISSILE #%d: already at/below ground — skipped.", missile_id)
            return

        t_impact = len(trajectory) * DT
        logger.info("  Predicted impact in %.1f s (%d integration steps)",
                    t_impact, len(trajectory))

        # ── Step 2: select the best intercept base ────────────────────────────
        base_idx, t_int, direction, int_pos = select_best_base(trajectory, BASES, DT)

        if base_idx is None:
            logger.warning(
                "t = 0.0 s | MISSILE #%d — INTERCEPT NOT POSSIBLE:"
                " no base can reach the missile before ground impact.",
                missile_id,
            )
            return

        # ── Step 3: report intercept parameters ───────────────────────────────
        travel_dist = float(np.linalg.norm(int_pos - BASES[base_idx]))

        logger.info(
            "t = 0.0 s | MISSILE #%d — BASE %d SELECTED for intercept",
            missile_id, base_idx + 1,
        )
        logger.info("  Intercept time     : %.1f s", t_int)
        logger.info("  Intercept position : [%8.0f, %8.0f, %8.0f] ENU m", *int_pos)
        logger.info("  Launch direction   : [%6.4f, %6.4f, %6.4f]", *direction)
        logger.info(
            "  Interceptor travel : %.0f m in %.1f s (avg %.0f m/s)",
            travel_dist, t_int, travel_dist / max(t_int, 1e-9),
        )
        logger.info("t = %.1f s | MISSILE #%d — INTERCEPT EVENT", t_int, missile_id)
