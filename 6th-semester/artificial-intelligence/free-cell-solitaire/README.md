# Assignment — FreeCell Solitaire Solver

Solves FreeCell Solitaire using BFS, DFS, Best-First Search, or A*.
Cards are moved from an 8-column tableau onto 4 foundation piles (A→K per suit)
using 4 temporary free cells as buffers.

## Course
Artificial Intelligence — Semester 6

## Language
Python 3.10+

## Algorithms

| Algorithm   | CLI flag  | Strategy                                              |
|-------------|-----------|-------------------------------------------------------|
| BFS         | `breadth` | Level-by-level exploration; shortest path in moves    |
| DFS         | `depth`   | Depth-first with cycle detection via visited set      |
| Best-First  | `best`    | Greedy heuristic h(n) (cards not yet on foundation)   |
| A*          | `astar`   | f(n) = h(n) + g(n) where g(n) is node depth          |

All algorithms enforce a 5-minute time limit and use a visited-state set to
avoid revisiting identical game states.

## Heuristic

```
h(n) = cards_in_tableau + cards_in_free_cells
       − cards_in_foundation − completed_piles
       − (cards_in_foundation / 4)
```

## How to Run

### Prerequisites
- Python 3.10+  (no third-party packages required)

### Steps
```bash
cd free-cell-solitaire
python main.py <algorithm> <input_file> <output_file>

# Examples:
python main.py breadth inputs/test21.txt outputs/bfs/solution21.txt
python main.py best    inputs/test22.txt outputs/best/solution22.txt
python main.py astar   inputs/test23.txt outputs/astar/solution23.txt
```

### Input Format
Each line represents one tableau column. The last card on each line is the
top card of that column. Cards are encoded as `<suit><rank>`, e.g. `H1` (Ace
of Hearts), `S13` (King of Spades).

### Output Format
```
Total moves to win: <N>, time: <T> minutes
freecell H5
stack D4 H5
source S1
...
```

## Project Structure
```
free-cell-solitaire/
├── main.py                          # argparse CLI entry point
├── requirements.txt
├── inputs/                          # sample board files
├── outputs/                         # sample solutions
├── game/                            # assignment PDF
└── src/
    └── freecell/
        ├── __init__.py
        ├── models.py       # GameState class (tableau, free cells, foundation)
        ├── algorithms.py   # BFS, DFS, Best-First, A*
        └── io.py           # read_tableau, write_solution
```

## What It Demonstrates
- OOP game state with deep-copy for immutable child generation
- Visited-state deduplication via serialised state strings
- Four search algorithms with a shared interface
- `logging` module replacing all `print()` calls
- `argparse` for structured CLI
- Type hints and Google-style docstrings throughout
