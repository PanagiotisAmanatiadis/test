# Knuth's Conjecture Solver

Solves Knuth's conjecture: any positive integer can be reached from **4**
using repeated application of factorial (n!), square root (√), and floor (⌊⌋).

## Course
Artificial Intelligence — Semester 6

## Language
C# 12 / .NET 8

## The Problem

| Operation    | Rule                                                    |
|--------------|---------------------------------------------------------|
| `factorial`  | n! — only when the state is a whole number and < 9 999 |
| `sqrt`       | √n — always applicable (result rounded to 3 sig. figs) |
| `floor`      | ⌊n⌋ — only when the state is fractional                |

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

## What It Demonstrates
- Tree-based search over an arithmetic state space
- BFS vs. Iterative Deepening trade-offs (memory vs. time)
- `ILogger<T>` injection via `Microsoft.Extensions.Logging`
- `sealed record` for immutable result type (`SearchResult`)
- `Queue<T>` for BFS, `Stack<T>` for depth-limited DFS
