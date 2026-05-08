# Lab 3 — Mutual Exclusion

Explores three levels of locking strategy in multithreaded C#: a single coarse
lock, per-element fine-grained locks, and deadlock-free synchronisation for the
classic Dining Philosophers problem.

## Course
Parallel and Distributed Computing — Semester 6

## Language
C# 12 / .NET 8

## Exercises

| # | Description |
|---|-------------|
| Q1 | **Coarse-grained locking** — one `lock` object guards the entire shared array; correct but limits concurrency |
| Q2 | **Fine-grained locking** — one `lock` object per array element; threads on different elements run truly in parallel |
| Q3 | **Dining Philosophers** — five philosophers, five forks; deadlock-free via resource ordering (highest-id philosopher picks up right fork first) |

## Key Concepts

### Coarse vs Fine-grained Locking

```
Coarse: lock(globalMutex) { array[i]++; }
        — only one thread can update ANY element at a time

Fine:   lock(locks[i])    { array[i]++; }
        — threads updating different elements run concurrently
```

### Dining Philosophers — Deadlock Prevention

Circular waiting is broken by resource ordering:
- Philosophers 0–3: pick up **left fork first**, then right
- Philosopher 4: picks up **right fork first**, then left

This ensures the cycle `0→1→2→3→4→0` can never form simultaneously.

## How to Run

### Prerequisites
- .NET 8 SDK

### Steps
```bash
cd Lab3/csharp
dotnet run
```

## C# Synchronisation Primitives Used
- `lock (obj) { ... }` — mutual exclusion block (syntactic sugar over `Monitor.Enter/Exit`)
- `Thread.Sleep(ms)` — simulate thinking/eating time
- `Random.Shared` — thread-safe random for non-deterministic delays
