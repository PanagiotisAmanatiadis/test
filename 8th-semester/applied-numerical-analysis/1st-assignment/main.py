"""Anti-missile system simulation for Thessaloniki — entry point.

Usage
-----
Single missile (default seed):
    python main.py

Five missiles with a custom seed:
    python main.py --missiles 5 --seed 99
"""

import argparse
import logging
import sys
from pathlib import Path

# Make the src/ package importable without installation
sys.path.insert(0, str(Path(__file__).parent / "src"))

from antimissile.simulation import Simulation

# ── Logging configuration ──────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%H:%M:%S",
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Thessaloniki anti-missile defence system simulation.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    p.add_argument(
        "--missiles", type=int, default=1,
        help="Number of incoming missiles to simulate.",
    )
    p.add_argument(
        "--seed", type=int, default=42,
        help="Random seed for reproducible missile generation.",
    )
    return p.parse_args()


def main() -> None:
    args = _parse_args()
    logger.info("Thessaloniki Anti-Missile Defence System")
    logger.info("  Missiles to simulate : %d", args.missiles)
    logger.info("  Random seed          : %d", args.seed)
    Simulation(seed=args.seed).run(n_missiles=args.missiles)
    logger.info("=" * 65)
    logger.info("Simulation complete.")


if __name__ == "__main__":
    main()
