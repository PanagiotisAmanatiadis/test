"""Regular 3-D Cartesian grid used by the Fast Marching Method."""

import numpy as np


class Grid:
    """Uniform 3-D grid over a cubic domain ``[lo, hi]^3``.

    All axes have the same spacing ``h = (hi - lo) / (n - 1)``.

    Args:
        n:      Number of grid points per axis (same for x, y, z).
        bounds: ``(lo, hi)`` extent along each axis.
    """

    def __init__(self, n: int = 50, bounds: tuple[float, float] = (-1.0, 1.0)) -> None:
        self.n        = n
        self.lo, self.hi = bounds
        self.h        = (self.hi - self.lo) / (n - 1)

        c = np.linspace(self.lo, self.hi, n)
        self.X, self.Y, self.Z = np.meshgrid(c, c, c, indexing="ij")

        # coords[i, j, k] = [x, y, z] of grid node (i, j, k)
        self.coords: np.ndarray = np.stack([self.X, self.Y, self.Z], axis=-1)

    def node_coords(self, i: int, j: int, k: int) -> np.ndarray:
        """Return the 3-D Cartesian coordinates of grid node ``(i, j, k)``.

        Args:
            i: Index along the x-axis.
            j: Index along the y-axis.
            k: Index along the z-axis.

        Returns:
            1-D array ``[x, y, z]``.
        """
        return self.coords[i, j, k]

    def __repr__(self) -> str:
        return (
            f"Grid(n={self.n}, bounds=({self.lo}, {self.hi}), h={self.h:.4f})"
        )
