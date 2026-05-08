# Lab 2 — Shared Variables & Race Conditions

Demonstrates how multiple threads accessing a shared variable without
synchronisation produce incorrect results (race conditions), and how a
`lock` statement eliminates those errors.

## Course
Parallel and Distributed Computing — Semester 6

## Language
C# 12 / .NET 8

## Exercises

### Exercise 1 — For-loop array counter

`N` threads each iterate over every index `0..End-1` and increment
`array[i]` exactly `i` times.
Expected after all threads join: `array[i] == N × i`.

| Variant | Description |
|---------|-------------|
| **Unsafe** | No synchronisation — threads race on `array[i]++` → wrong values |
| **Safe**   | `lock` around every increment → always 0 errors |

### Exercise 2 — While-loop index counter

Threads share a global index counter. Each iteration a thread claims the
current index, writes to that cell, then increments the counter.
Expected: every cell equals `1` (written exactly once).

| Variant | Description |
|---------|-------------|
| **Unsafe** | No synchronisation — two threads can claim the same index → duplicate writes, missed cells |
| **Safe**   | `lock` wraps the entire check–write–increment → always 0 errors |

## Sharing Strategies Illustrated

| Strategy | How state is shared |
|----------|---------------------|
| **Global static** | Accessed directly via static fields |
| **Constructor args** | `SharedArrayState` passed to each worker at construction time |
| **Shared object** | Single `SharedArrayState` instance referenced by all workers |

## How to Run

### Prerequisites
- .NET 8 SDK

### Steps
```bash
cd Lab2/csharp
dotnet run
```

## Key C# Concepts

- **Race condition** — two threads read-modify-write the same variable concurrently without coordination
- `lock (obj) { ... }` — mutual exclusion; only one thread executes the block at a time
- `Interlocked.Increment(ref x)` — atomic increment without a full `lock` (shown in Program comments)
- `Thread.Join()` — wait for a thread to finish before checking results
