"""
Movie Recommender System — entry point.

Usage examples
--------------
Run all three models with default settings:
    python main.py

Run only User-CF with K=20 and 80/20 split:
    python main.py --model user --k 20 --test-frac 0.2

Run SVD with 100 latent factors:
    python main.py --model svd --n-factors 100

Specify a custom dataset path:
    python main.py --data path/to/ratings.csv
"""

import argparse
import logging
import sys
from pathlib import Path

from recommender.data import DataLoader
from recommender.evaluation import Evaluator
from recommender.models import ItemBasedCF, SVDRecommender, UserBasedCF
from recommender.models.base import BaseRecommender

# ── logging setup ─────────────────────────────────────────────────────────────

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
        description="Movie recommender system — collaborative filtering and SVD",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--data",
        type=Path,
        default=Path("dataset.csv"),
        help="Path to the ratings CSV file.",
    )
    parser.add_argument(
        "--model",
        choices=["user", "item", "svd", "all"],
        default="all",
        help="Which model(s) to train and evaluate.",
    )
    parser.add_argument(
        "--k",
        type=int,
        default=30,
        help="Number of nearest neighbours for User-CF and Item-CF.",
    )
    parser.add_argument(
        "--n-factors",
        type=int,
        default=50,
        help="Number of latent factors for SVD.",
    )
    parser.add_argument(
        "--test-frac",
        type=float,
        default=0.2,
        help="Fraction of ratings to hold out for testing (stratified by user).",
    )
    parser.add_argument(
        "--min-user-ratings",
        type=int,
        default=50,
        help="Minimum number of ratings a user must have to be included.",
    )
    parser.add_argument(
        "--min-movie-ratings",
        type=int,
        default=50,
        help="Minimum number of ratings a movie must have to be included.",
    )
    return parser.parse_args()


# ── main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    args = parse_args()

    # ── load and split data ───────────────────────────────────────────────────
    loader = DataLoader(
        min_user_ratings=args.min_user_ratings,
        min_movie_ratings=args.min_movie_ratings,
    )
    ratings = loader.load(args.data)
    split   = loader.split(ratings, test_frac=args.test_frac)

    evaluator = Evaluator()
    results   = []

    # ── build model list ──────────────────────────────────────────────────────
    models: list[tuple[str, BaseRecommender]] = []

    if args.model in ("user", "all"):
        models.append(("User-CF  (k=%d)" % args.k, UserBasedCF(k=args.k)))
    if args.model in ("item", "all"):
        models.append(("Item-CF  (k=%d)" % args.k, ItemBasedCF(k=args.k)))
    if args.model in ("svd", "all"):
        models.append(("SVD  (factors=%d)" % args.n_factors, SVDRecommender(n_factors=args.n_factors)))

    # ── train → evaluate ──────────────────────────────────────────────────────
    for name, model in models:
        logger.info("=" * 60)
        logger.info("Model: %s", name)
        model.fit(split.train)
        result = evaluator.evaluate(model, split.test, model_name=name)
        results.append(result)

    # ── summary table ─────────────────────────────────────────────────────────
    print()
    print("=" * 65)
    print(" RESULTS SUMMARY")
    print("=" * 65)
    header = f"{'Model':<25} {'MAE':>6} {'RMSE':>6} {'Prec':>6} {'Recall':>6} {'F1':>6} {'Cov':>6}"
    print(header)
    print("-" * 65)
    for r in results:
        row = (
            f"{r.model_name:<25} "
            f"{r.mae:>6.3f} "
            f"{r.rmse:>6.3f} "
            f"{r.precision:>6.3f} "
            f"{r.recall:>6.3f} "
            f"{r.f1:>6.3f} "
            f"{r.coverage:>5.1%}"
        )
        print(row)
    print("=" * 65)


if __name__ == "__main__":
    main()
