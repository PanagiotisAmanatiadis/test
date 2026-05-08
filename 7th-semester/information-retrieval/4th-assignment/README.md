# Assignment 4 — Movie Recommender System

Collaborative filtering and matrix factorisation recommender built on the
MovieLens-style ratings dataset.  Three algorithms are implemented and compared
on MAE, RMSE, Precision, Recall, and F1.

## Course
Information Retrieval — Semester 7

## Language
Python 3.11+

## Algorithms

| Model | Technique | Similarity / Decomposition |
|-------|-----------|---------------------------|
| **User-CF** | Memory-based user-user CF | Mean-centered cosine similarity (≈ Pearson) |
| **Item-CF** | Memory-based item-item CF | Adjusted cosine similarity (user-mean centering) |
| **SVD** | Model-based matrix factorisation | Truncated SVD with user/item bias terms |

### User-Based Collaborative Filtering

```
pred(u, i) = μ_u + Σ_v [ sim(u,v) × (r_vi − μ_v) ] / Σ_v |sim(u,v)|
```

Selects the K most similar users who have rated item *i*.  Mean-centering
before cosine similarity removes scale differences between users.

### Item-Based Collaborative Filtering

```
pred(u, i) = Σ_j [ sim(i,j) × r_uj ] / Σ_j |sim(i,j)|
```

Uses adjusted cosine (user-mean subtracted) for item similarity.
Selects the K most similar items the target user has already rated.

### SVD Matrix Factorisation

```
R ≈ μ + B_u + B_i + U × Σ × V^T
```

The residual matrix (ratings minus biases) is decomposed by `TruncatedSVD`
from scikit-learn.  The reconstructed matrix gives a dense rating prediction
for any (user, item) pair seen during training.

## Dataset

`dataset.csv` — 100 836 ratings by 610 users on 9 724 movies (0.5–5.0 scale).
Format: `userId, movieId, rating, timestamp`.

## Project Structure

```
4th-assignment/
├── src/
│   └── recommender/
│       ├── __init__.py
│       ├── data.py           # DataLoader: load, filter, stratified split
│       ├── evaluation.py     # Evaluator + EvalResult (MAE, RMSE, P/R/F1, Coverage)
│       └── models/
│           ├── __init__.py
│           ├── base.py       # BaseRecommender ABC
│           ├── user_cf.py    # UserBasedCF
│           ├── item_cf.py    # ItemBasedCF
│           └── svd.py        # SVDRecommender
├── main.py                   # CLI entry point
├── requirements.txt
└── README.md
```

## How to Run

### Prerequisites
```bash
pip install -r requirements.txt
```

### Run all models (default settings)
```bash
cd 4th-assignment
python main.py
```

### CLI options
```
--data            Path to CSV file          (default: dataset.csv)
--model           user | item | svd | all   (default: all)
--k               Nearest neighbours K      (default: 30)
--n-factors       SVD latent factors        (default: 50)
--test-frac       Test split fraction       (default: 0.2)
--min-user-ratings  Activity filter         (default: 50)
--min-movie-ratings Activity filter         (default: 50)
```

### Examples
```bash
# Only run SVD with 100 latent factors
python main.py --model svd --n-factors 100

# User-CF with K=20 and 80/20 split
python main.py --model user --k 20 --test-frac 0.2

# Looser activity filter (more users and movies)
python main.py --min-user-ratings 20 --min-movie-ratings 20
```

## Improvements Over the Original

| Original | Refactored |
|----------|-----------|
| All code at module level, procedural | OOP package: `DataLoader`, `BaseRecommender`, `Evaluator` |
| `DataFrame.append()` (removed in pandas 2.0) | `pd.concat` / vectorised numpy |
| O(n²) Python loop for similarities | Vectorised `sklearn.metrics.pairwise.cosine_similarity` |
| Hard-coded file path `ratings.csv` | `argparse` `--data` flag |
| `input()` prompts | Command-line arguments with defaults |
| Buggy loop variable shadowing | Clean scoping |
| MAE + basic P/R only | MAE, RMSE, Precision, Recall, F1, Coverage |
| One algorithm (User-CF) | Three algorithms: User-CF, Item-CF, SVD |
| No train/test integrity | Stratified split — every user in both sets |
| No logging | Structured `logging` throughout |
