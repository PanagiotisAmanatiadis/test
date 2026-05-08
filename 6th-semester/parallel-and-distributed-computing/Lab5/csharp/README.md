# Lab 5 — Data Parallelism

Demonstrates data-parallel patterns where independent array elements can be
processed concurrently by splitting the index space across threads.

## Course
Parallel and Distributed Computing — Semester 6

## Language
C# 12 / .NET 8

## Exercises

| # | Problem | Parallelisation strategy |
|---|---------|--------------------------|
| Q1 | **Vector Addition** `a[i] = b[i] + c[i]` (1 M doubles) | Partition index range; each thread adds its slice |
| Q2 | **Matrix Addition** `a[i,j] = b[i,j] + c[i,j]` (1000×1000) | Partition by rows |
| Q3 | **RGB → Grayscale** `gray = 0.299R + 0.587G + 0.114B` (1920×1080) | Partition pixel rows |
| Q4 | **SAT Solver** — evaluate Boolean circuit over 2²⁰ inputs | Partition integer range; collect results in `ConcurrentBag<int>` |

Each exercise prints sequential and parallel elapsed times for direct comparison.

## Key C# Concepts

- **Manual thread partitioning** — `ParallelRunner.For(total, numThreads, body)` splits `[0, total)` into equal chunks and starts one thread per chunk
- **No synchronisation needed** — threads write to disjoint array regions
- **`ConcurrentBag<T>`** — thread-safe collection for the SAT results (multiple writers, no ordering guarantee)
- Contrast with `Parallel.For` (TPL) which does the same partitioning automatically

## How to Run

### Prerequisites
- .NET 8 SDK

### Steps
```bash
cd Lab5/csharp
dotnet run
```
