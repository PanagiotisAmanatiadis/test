# Assignment — Peg Solitaire Solver

Solves Peg Solitaire boards using Depth-First Search or Best-First Search.
A peg can jump over an adjacent peg into an empty hole, removing the jumped peg.
The goal is to reduce the board to a single peg.

## Course
Artificial Intelligence — Semester 6

## Language
Python 3.10+

## Algorithms

| Algorithm   | CLI flag | Heuristic                                    |
|-------------|----------|----------------------------------------------|
| DFS         | `depth`  | None — pure depth-first exploration          |
| Best-First  | `best`   | Remaining peg count (fewer pegs = better)    |

Both algorithms enforce a 60-second time limit.

## How to Run

### Prerequisites
- Python 3.10+  (no third-party packages required)

### Steps
```bash
cd peg-solitaire
python main.py <algorithm> <input_file> <output_file>

# Examples:
python main.py depth  inputs/test1.txt outputs/dfs/solution1.txt
python main.py best   inputs/test1.txt outputs/best/solution1.txt
```

### Input Format
Each line is a space-separated row of the board.
`1` = peg, `2` = empty hole.
The first line is a metadata/header line and is skipped.

### Output Format
```
<number_of_moves>
x y x' y'   ← source (x,y) → destination (x',y') for each move
...
```

## Project Structure
```
peg-solitaire/
├── main.py                         # argparse CLI entry point
├── requirements.txt
├── inputs/                         # sample board files
├── outputs/                        # sample solutions
├── game/                           # assignment PDF
└── src/
    └── peg_solver/
        ├── __init__.py
        ├── models.py       # SearchNode class (board state + expansion)
        ├── algorithms.py   # depth_first_search, best_first_search
        └── io.py           # read_board, write_solution
```

## What It Demonstrates
- OOP encapsulation: board state and move generation inside `SearchNode`
- `logging` module replacing all `print()` calls
- `argparse` for structured CLI
- Type hints on all function signatures
- Google-style docstrings
