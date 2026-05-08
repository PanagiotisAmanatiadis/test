"""
Instance Selection — IB2 and ENN entry point.

Usage
-----
Run both algorithms on both datasets (defaults):
    python main.py

Custom dataset paths:
    python main.py --iris path/to/iris.csv --letters path/to/letter-recognition.csv

Save output to a custom directory:
    python main.py --output-dir results/
"""

import argparse
import logging
import sys
from pathlib import Path

from instance_selection.data import DataLoader
from instance_selection.selectors import ENNSelector, IB2Selector

# ── logging ───────────────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
    datefmt="%H:%M:%S",
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)

# ── CLI ───────────────────────────────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="IB2 and ENN instance selection on Iris and Letter-Recognition datasets.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--iris",    type=Path, default=Path("iris.csv"))
    parser.add_argument("--letters", type=Path, default=Path("letter-recognition.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("."),
                        help="Directory where output CSVs are written.")
    parser.add_argument("--enn-k", type=int, default=3,
                        help="Number of neighbours for ENN.")
    parser.add_argument("--ib2-only",  action="store_true", help="Run IB2 only.")
    parser.add_argument("--enn-only",  action="store_true", help="Run ENN only.")
    return parser.parse_args()


# ── main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    loader  = DataLoader()
    iris    = loader.load(args.iris,    name="iris")
    letters = loader.load(args.letters, name="letter-recognition")

    run_ib2 = not args.enn_only
    run_enn = not args.ib2_only

    results: list[tuple[str, int, int]] = []

    if run_ib2:
        logger.info("=" * 55)
        logger.info("Running IB2")
        logger.info("=" * 55)
        ib2 = IB2Selector()

        for dataset in (iris, letters):
            selected = ib2.select(dataset)
            out_path = args.output_dir / f"{dataset.name}IB2.csv"
            selected.to_dataframe().to_csv(out_path, index=False)
            logger.info("Saved → %s", out_path)
            results.append((f"{dataset.name} IB2", len(dataset.X), len(selected.X)))

    if run_enn:
        logger.info("=" * 55)
        logger.info("Running ENN  (k=%d)", args.enn_k)
        logger.info("=" * 55)
        enn = ENNSelector(k=args.enn_k)

        for dataset in (iris, letters):
            selected = enn.select(dataset)
            out_path = args.output_dir / f"{dataset.name}ENN.csv"
            selected.to_dataframe().to_csv(out_path, index=False)
            logger.info("Saved → %s", out_path)
            results.append((f"{dataset.name} ENN", len(dataset.X), len(selected.X)))

    # ── summary ───────────────────────────────────────────────────────────────
    logger.info("=" * 52)
    logger.info(" SUMMARY")
    logger.info("=" * 52)
    logger.info("%-28s %7s %7s %7s", "Algorithm", "Before", "After", "Kept")
    logger.info("-" * 52)
    for label, before, after in results:
        kept_pct = 100 * after / before if before > 0 else 0.0
        logger.info("%-28s %7d %7d %6.1f%%", label, before, after, kept_pct)
    logger.info("=" * 52)


if __name__ == "__main__":
    main()
