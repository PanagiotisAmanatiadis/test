"""Analytic Signed Distance Functions (SDF) for test geometries.

A Signed Distance Function returns a negative value for points inside the
shape and a positive value for points outside; its magnitude equals the
shortest distance to the surface.

All ``sdf`` methods accept NumPy arrays of arbitrary leading shape with a
trailing axis of size 3 (e.g. shape ``(N, N, N, 3)`` from a grid), enabling
fully vectorised evaluation.
"""

from __future__ import annotations

import numpy as np


class Sphere:
    """Sphere centred at *center* with given *radius*.

    Args:
        center: Centre coordinates, shape (3,).
        radius: Sphere radius (must be > 0).
    """

    def __init__(self, center: np.ndarray, radius: float) -> None:
        self.center = np.asarray(center, dtype=float)
        self.radius = float(radius)

    def sdf(self, points: np.ndarray) -> np.ndarray:
        """Compute the SDF at *points*.

        Args:
            points: Array of shape ``(..., 3)``.

        Returns:
            SDF values with shape matching the leading dimensions of *points*.
            Negative inside, positive outside.
        """
        return np.linalg.norm(points - self.center, axis=-1) - self.radius

    def __str__(self) -> str:
        return f"Sphere(center={self.center.tolist()}, radius={self.radius})"

    def __repr__(self) -> str:
        return self.__str__()


class Box:
    """Axis-aligned box (rectangular cuboid) centred at *center*.

    Args:
        center:       Centre coordinates, shape (3,).
        half_extents: Half-width along each axis — scalar (cube) or shape (3,).
    """

    def __init__(
        self,
        center: np.ndarray,
        half_extents: float | np.ndarray,
    ) -> None:
        self.center       = np.asarray(center, dtype=float)
        self.half_extents = np.broadcast_to(half_extents, (3,)).astype(float)

    def sdf(self, points: np.ndarray) -> np.ndarray:
        """Compute the SDF at *points*.

        Uses the standard box SDF formula::

            q = |p - center| - half_extents
            SDF = ||max(q, 0)|| + min(max(q_x, q_y, q_z), 0)

        Args:
            points: Array of shape ``(..., 3)``.

        Returns:
            SDF values with shape matching the leading dimensions of *points*.
        """
        q = np.abs(points - self.center) - self.half_extents
        return (
            np.linalg.norm(np.maximum(q, 0.0), axis=-1)
            + np.minimum(np.max(q, axis=-1), 0.0)
        )

    def __str__(self) -> str:
        return f"Box(center={self.center.tolist()}, half_extents={self.half_extents.tolist()})"

    def __repr__(self) -> str:
        return self.__str__()
