# Assignment 3 — Instance Selection: IB2 & ENN

Implements two classic instance selection algorithms from the KDD literature
and applies them to the Iris and Letter-Recognition datasets.

## Course
Knowledge Discovery from Databases — Semester 7

## Language
Python 3.11+

## Algorithms

### IB2 — Instance-Based Learning 2 (Aha, Kibler & Albert, 1991)

Builds a minimal **concept set** (CS) in a single pass:

1. Initialise CS with the first instance.
2. For each remaining instance *p*: classify *p* with 1-NN from CS.
   - If misclassified → add *p* to CS (it carries new information).
   - If correctly classified → discard (redundant).

The result is the smallest subset that self-consistently explains all
retained instances under the 1-NN rule.

### ENN — Edited Nearest Neighbour (Wilson, 1972)

Removes noisy / borderline instances:

For each instance *p*, find its *k* = 3 nearest neighbours (excluding itself).
If fewer than half of them share *p*'s class label, *p* is removed.

```
remove p  ⟺  same-class fraction among k-NN < 0.5
```

## Datasets

| Dataset | Instances | Features | Classes |
|---------|-----------|----------|---------|
| `iris.csv` | 150 | 4 | 3 |
| `letter-recognition.csv` | 20 000 | 16 | 26 |

Features are scaled to [0, 1] with MinMax normalisation before selection.

## Results

| Algorithm | Dataset | Before | After | Retained |
|-----------|---------|--------|-------|----------|
| IB2 | Iris | 150 | 7 | 4.7 % |
| IB2 | Letter-Recognition | 20 000 | 2 730 | 13.7 % |
| ENN | Iris | 150 | 143 | 95.3 % |
| ENN | Letter-Recognition | 20 000 | 19 110 | 95.5 % |

## Project Structure

```
3rd-assignment/
├── src/
│   └── instance_selection/
│       ├── __init__.py
│       ├── data.py                # DataLoader + Dataset dataclass
│       └── selectors/
│           ├── __init__.py
│           ├── base.py            # BaseInstanceSelector ABC + vectorised k-NN helper
│           ├── ib2.py             # IB2Selector
│           └── enn.py             # ENNSelector (batch NearestNeighbors)
├── main.py                        # CLI entry point
├── requirements.txt
└── README.md
```

## How to Run

### Prerequisites
```bash
pip install -r requirements.txt
```

### Run both algorithms on both datasets
```bash
cd 3rd-assignment
python main.py
```

### CLI options
```
--iris          Path to Iris CSV              (default: iris.csv)
--letters       Path to Letter-Recognition CSV (default: letter-recognition.csv)
--output-dir    Directory for output CSVs      (default: .)
--enn-k         Number of neighbours for ENN   (default: 3)
--ib2-only      Run IB2 only
--enn-only      Run ENN only
```

## Improvements Over the Original

| Original | Refactored |
|----------|-----------|
| All code at module level | OOP package: `DataLoader`, `BaseInstanceSelector`, `IB2Selector`, `ENNSelector` |
| `DataFrame.append()` (removed in pandas 2.0) | Index list accumulated; sliced once with `X[cs_indices]` |
| O(n²) Python loop in ENN (45 s on letters) | Batch `NearestNeighbors` (sklearn KD-tree): **2 s** |
| O(n·k) selection-sort in `k_nearest` | `np.argpartition` for O(n + k·log k) top-k |
| Buggy index access after `.drop()` | Numpy index arrays — no fragile DataFrame indexing |
| Hard-coded filenames | `argparse` `--iris`, `--letters`, `--output-dir` |
| No logging | Structured `logging` with timing |
| No type hints or docstrings | Full type annotations and Google-style docstrings |
