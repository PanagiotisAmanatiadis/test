# Lab 8 — Divide-and-Conquer Parallelism

Demonstrates recursive divide-and-conquer applied to parallel numerical
integration and parallel sorting, with threshold-based cutoffs to avoid
excessive thread creation.

## Course
Parallel and Distributed Computing — Semester 6

## Language
C# 12 / .NET 8

## Exercises

### Exercise 1 — Pi via Recursive Integration

```
IntegrateParallel(lo, hi):
    if hi - lo ≤ threshold → sequential loop
    mid = (lo + hi) / 2
    spawn thread → IntegrateParallel(mid, hi)
    compute        IntegrateParallel(lo,  mid)
    join thread
    return left + right
```

- Threshold: 500 000 steps → roughly log₂(20) = ~4 recursion levels
- No shared mutable state — each recursive call accumulates into its own local `double`

### Exercise 2 — Parallel Merge Sort

```
ParallelSort(arr, l, r, depth):
    if depth < MaxParallelDepth:
        spawn thread → ParallelSort(arr, m+1, r, depth+1)
        ParallelSort(arr, l, m, depth+1)    ← this thread
        join thread
    else:
        SequentialSort both halves
    Merge(arr, l, m, r)                     ← always sequential
```

- `MaxParallelDepth = 3` → up to 8 concurrent threads at the leaf level
- Array size: 4 M integers, randomly generated

## Key C# Concepts

- Recursive thread spawning with a depth limit
- Closure capture of `rightResult` inside a `Thread` lambda
- `arr[l..(m+1)]` — range syntax for slice copy
- `IsSorted()` — O(n) correctness check after sort

## How to Run

### Prerequisites
- .NET 8 SDK

### Steps
```bash
cd Lab8/csharp
dotnet run
```
