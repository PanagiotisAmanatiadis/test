"""3-D distance computation via Fast Marching Method — entry point.

Computes the Signed Distance Function (SDF) for two geometric shapes on a
uniform 3-D grid and verifies accuracy against the closed-form analytic SDF.

Usage
-----
Default run (50³ grid, sphere + cube, save PNG slices to current directory):
    python main.py

Higher resolution without plots:
    python main.py --grid-size 80 --no-plot

Custom output directory:
    python main.py --output-dir results/
"""

import argparse
import logging
import sys
from pathlib import Path

# Make the src/ package importable without installation
sys.path.insert(0, str(Path(__file__).parent / "src"))

import numpy as np

from fmm3d.grid import Grid
from fmm3d.shapes import Sphere, Box
from fmm3d.fmm import compute_signed_distance
from fmm3d.visualizer import plot_slices

# ── Logging configuration ──────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
    datefmt="%H:%M:%S",
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="3-D distance field computation via Fast Marching Method.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    p.add_argument(
        "--grid-size", type=int, default=50,
        help="Number of grid points per axis (N; total nodes = N³).",
    )
    p.add_argument(
        "--bounds", type=float, default=1.0,
        help="Domain extent: grid spans [-b, b]³.",
    )
    p.add_argument(
        "--no-plot", action="store_true",
        help="Skip all visualisation (useful in headless environments).",
    )
    p.add_argument(
        "--output-dir", type=Path, default=Path("."),
        help="Directory for output PNG slice plots.",
    )
    return p.parse_args()


def _run_shape(grid: Grid, shape, label: str, args: argparse.Namespace) -> None:
    """Run FMM for *shape*, report accuracy, and optionally save a slice plot.

    Args:
        grid:  Computational grid.
        shape: Shape object with a vectorised ``sdf`` method.
        label: Human-readable name used in log messages and the output filename.
        args:  Parsed command-line arguments.
    """
    logger.info("=" * 60)
    logger.info("Shape  : %s", shape)

    # Evaluate the analytic SDF at every grid node (vectorised)
    analytic_sdf = shape.sdf(grid.coords)   # shape: (N, N, N)

    # Run the Fast Marching Method
    fmm_sdf = compute_signed_distance(grid, analytic_sdf)

    # Accuracy check: mean absolute error against the analytic SDF
    rng    = np.random.default_rng(0)
    sample = rng.integers(0, grid.n, size=(500, 3))
    exact  = analytic_sdf[sample[:, 0], sample[:, 1], sample[:, 2]]
    fmm    = fmm_sdf[sample[:, 0], sample[:, 1], sample[:, 2]]
    mae    = float(np.mean(np.abs(exact - fmm)))
    logger.info("Accuracy (MAE vs analytic): %.6f over 500 random nodes", mae)
    logger.info("Grid spacing h = %.4f — expected O(h) error ≈ %.4f", grid.h, grid.h)

    if not args.no_plot:
        safe_label = label.lower().replace(" ", "_").replace("=", "").replace(".", "p")
        out = args.output_dir / f"sdf_{safe_label}.png"
        plot_slices(grid, fmm_sdf, title=f"SDF — {label}", output_path=out)


def main() -> None:
    args = _parse_args()

    grid = Grid(n=args.grid_size, bounds=(-args.bounds, args.bounds))
    logger.info("Grid: %d³ nodes | h = %.4f | domain [%.1f, %.1f]³",
                grid.n, grid.h, grid.lo, grid.hi)

    # ── Assignment shape: sphere at origin with R = 0.3 ───────────────────────
    _run_shape(grid, Sphere(np.zeros(3), 0.3), "Sphere R=0.3", args)

    # ── Additional test: axis-aligned cube ────────────────────────────────────
    _run_shape(grid, Box(np.zeros(3), 0.25), "Cube half=0.25", args)

    logger.info("=" * 60)
    logger.info("All shapes processed. Done.")


if __name__ == "__main__":
    main()
