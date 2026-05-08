# Lab 6 — Pi Computation & Parallel String Matching

Demonstrates reduction patterns in parallel computing: aggregating partial
results from multiple threads without heavy synchronisation.

## Course
Parallel and Distributed Computing — Semester 6

## Language
C# 12 / .NET 8

## Exercises

### Exercise 1 — Pi via Numerical Integration

Approximates π by integrating `4 / (1 + x²)` over [0, 1] with 10 M steps.

| Variant | Synchronisation | Notes |
|---------|----------------|-------|
| Sequential | — | Baseline |
| Parallel + shared `lock` | `lock` on every step | Correct but high contention |
| Parallel + local reduction | None during computation | Each thread writes to its own `partials[tid]` slot; main thread sums after join |

### Exercise 2 — Brute-force String Matching

Scans a 1 M character text for all occurrences of a pattern.

- **Sequential**: O(n·m) nested loop
- **Parallel**: position range `[0, n-m)` partitioned across 4 threads; each thread appends matches to `ConcurrentBag<int>`

## Key C# Concepts

- **Per-thread local array slot** — `partials[tid]` avoids false sharing and lock overhead
- `double[].Sum()` — aggregation step after `Join()` (sequential, no sync needed)
- `ConcurrentBag<T>` — thread-safe unordered collection for concurrent inserts
- `Stopwatch` for elapsed-time measurement

## How to Run

### Prerequisites
- .NET 8 SDK

### Steps
```bash
cd Lab6/csharp
dotnet run
```
