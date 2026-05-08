"""ODE system and 4th-order Runge-Kutta integrator for the incoming missile.

The missile is subject to:
  * Gravity:       g = [0, 0, -9.81] m/s²
  * Thrust force:  F_th = 5 000 N, applied along the instantaneous velocity direction
  * Aerodynamic drag: F_drag = -0.5 * Cd * rho * A * ||v|| * v

The state vector is ``s = [x, y, z, vx, vy, vz]`` in the local ENU frame.
"""

import numpy as np

# ── Physical parameters ────────────────────────────────────────────────────────
_G_VEC     = np.array([0.0, 0.0, -9.81])   # gravity [m/s²]
_F_TH      = 5_000.0                        # thrust magnitude [N]
_MASS      = 1_000.0                        # missile mass [kg]
_AREA      = 1.0                            # frontal area [m²]
_CD        = 0.5                            # drag coefficient
_RHO       = 1.225                          # air density [kg/m³]

# Pre-computed scalars for the ODE
_THRUST_ACC  = _F_TH / _MASS                           # [m/s²]
_DRAG_COEFF  = 0.5 * _CD * _RHO * _AREA / _MASS       # [1/m]


def _ode(state: np.ndarray) -> np.ndarray:
    """Right-hand side of the missile ODE.

    Computes ``ds/dt = f(s)`` where::

        dv/dt = g + (F_th/m) * v̂ - (Cd*rho*A)/(2m) * ||v|| * v
        dr/dt = v

    Args:
        state: State vector ``[x, y, z, vx, vy, vz]``, shape (6,).

    Returns:
        Time derivative ``[vx, vy, vz, ax, ay, az]``, shape (6,).
    """
    v      = state[3:]
    v_norm = float(np.linalg.norm(v))

    # Thrust acts along the current velocity direction
    thrust_acc = _THRUST_ACC * (v / v_norm) if v_norm > 1e-12 else np.zeros(3)

    # Drag decelerates proportional to speed squared (split as ||v|| * v for vectorial form)
    drag_acc = -_DRAG_COEFF * v_norm * v

    accel = _G_VEC + thrust_acc + drag_acc
    return np.concatenate([v, accel])


def rk4_step(state: np.ndarray, dt: float) -> np.ndarray:
    """Advance the missile state by one 4th-order Runge-Kutta step.

    Args:
        state: Current state vector ``[x, y, z, vx, vy, vz]``, shape (6,).
        dt:    Time step size in seconds.

    Returns:
        New state vector after *dt* seconds, shape (6,).
    """
    k1 = _ode(state)
    k2 = _ode(state + 0.5 * dt * k1)
    k3 = _ode(state + 0.5 * dt * k2)
    k4 = _ode(state + dt * k3)
    return state + (dt / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)
