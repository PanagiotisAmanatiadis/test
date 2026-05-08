"""2-D cross-section visualisation of a 3-D signed distance field.

Produces a figure with three orthogonal slices (yz-, xz-, and xy-planes
through the grid midpoint), colour-mapped with a diverging palette so that
the zero level-set (the surface) stands out clearly.
"""

from __future__ import annotations

import logging
from pathlib import Path

import numpy as np

logger = logging.getLogger(__name__)


def plot_slices(
    grid,
    dist: np.ndarray,
    title: str = "Signed Distance Field",
    output_path: Path | None = None,
) -> None:
    """Render three orthogonal cross-sections of *dist* and save or display.

    Args:
        grid:        Grid object used for the computation (provides ``n``, ``lo``, ``hi``).
        dist:        Signed distance array, shape ``(N, N, N)``.
        title:       Figure super-title.
        output_path: If given, save the figure as a PNG to this path.
                     If *None*, call ``plt.show()`` interactively.
    """
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        logger.error(
            "matplotlib is not installed. Run: pip install matplotlib"
        )
        return

    n   = grid.n
    mid = n // 2
    lo, hi = grid.lo, grid.hi
    extent = [lo, hi, lo, hi]

    vmax = float(np.nanmax(np.abs(dist)))
    vmin = -vmax

    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))
    fig.suptitle(title, fontsize=13, fontweight="bold")

    axis_labels = [
        ("y (m)", "z (m)", "yz-plane  x ≈ 0",  dist[mid, :, :].T),
        ("x (m)", "z (m)", "xz-plane  y ≈ 0",  dist[:, mid, :].T),
        ("x (m)", "y (m)", "xy-plane  z ≈ 0",  dist[:, :, mid].T),
    ]

    for ax, (xlabel, ylabel, subtitle, data) in zip(axes, axis_labels):
        im = ax.imshow(
            data,
            origin="lower",
            extent=extent,
            cmap="RdBu_r",
            vmin=vmin,
            vmax=vmax,
            interpolation="bilinear",
        )
        # Overlay the zero level-set contour (the surface)
        ticks = np.linspace(lo, hi, n)
        ax.contour(ticks, ticks, data, levels=[0.0], colors="k", linewidths=1.5)
        ax.set_title(subtitle, fontsize=10)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04, label="SDF [m]")

    plt.tight_layout()

    if output_path is not None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(output_path, dpi=150, bbox_inches="tight")
        logger.info("Slice plot saved → %s", output_path)
    else:
        plt.show()

    plt.close(fig)
