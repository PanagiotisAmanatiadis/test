# Knuth's Conjecture Solver (C#)

C# port of the Knuth conjecture solver, implementing BFS and Iterative Deepening Search.

## Course
Artificial Intelligence — Semester 6

## Language
C# 12 / .NET 8 — Console application

## The Problem

**Knuth's conjecture** states that any positive integer can be reached starting
from **4** by repeatedly applying three operations:

| Operation    | Rule                                                    |
|--------------|---------------------------------------------------------|
| `factorial`  | n! — only when the state is a whole number and < 9 999 |
| `sqrt`       | √n — always applicable (result rounded to 3 sig. figs) |
| `floor`      | ⌊n⌋ — only when the state is fractional                |

The solver finds a sequence of operations that transforms **4** into the target.

## Algorithms

| Algorithm            | Time limit | Description                                              |
|----------------------|------------|----------------------------------------------------------|
| BFS                  | 60 s       | Breadth-First Search — guarantees shortest-move solution |
| ID (Iterative Deep.) | 30 s       | Depth-limited DFS with increasing depth bounds           |

## How to Run

### Prerequisites
- .NET 8 SDK

### Steps
```bash
cd knuth/csharp
dotnet run
```

The program prompts interactively:
```
Search method (BFS or ID): BFS
Goal number (positive integer): 5
Output file (default: result.txt): result.txt
```

## Project Structure
```
csharp/
├── src/
│   ├── Models/
│   │   └── SearchNode.cs    # Search tree node with state and expansion logic
│   ├── Services/
│   │   ├── Algorithms.cs    # BFS and Iterative Deepening implementations
│   │   └── SearchResult.cs  # Result record (moves, elapsed time, solved flag)
│   └── Program.cs           # Interactive CLI entry point
└── KnuthSolver.csproj
```

## What It Demonstrates
- `ILogger<T>` injection via `Microsoft.Extensions.Logging`
- `sealed record` for immutable result type
- `Queue<T>` for BFS, `Stack<T>` for depth-limited DFS
- Null-safe C# 12 patterns (`is not null`, pattern matching)
- XML doc comments on all public members
