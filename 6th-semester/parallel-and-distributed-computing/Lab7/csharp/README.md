# Lab 7 — Histogram, Word Count & Sieve of Eratosthenes

Explores three load-balancing strategies for parallel algorithms and demonstrates
the reduce pattern with local accumulators.

## Course
Parallel and Distributed Computing — Semester 6

## Language
C# 12 / .NET 8

## Exercises

### Exercise 1 — Character Frequency Histogram

Counts character occurrences in a 5 M character text.

- Each thread fills a local `int[128]` for its slice — zero contention
- After `Join()`, local arrays are summed in O(128 × N) time

### Exercise 2 — Word Count

Counts words (whitespace-delimited) in the same text.

- Threads count words in their slice independently
- Boundary correction: if a slice starts mid-word the count is decremented by 1

### Exercise 3 — Sieve of Eratosthenes (limit = 10 M)

| Strategy | How work is assigned |
|----------|----------------------|
| **Static** | Range divided equally among threads at startup |
| **Cyclic** | Thread `t` handles every `N`-th candidate starting at offset `t` |
| **Dynamic** | Threads atomically claim the next `ChunkSize`-sized block via `Interlocked.Add` |

**Dynamic scheduling** avoids load imbalance when some chunks are harder (e.g., dense composite regions).

## Key C# Concepts

- **Local accumulator arrays** — `locals[tid]` avoids contention during histogram counting
- `Interlocked.Add(ref counter, delta)` — atomic fetch-and-add for dynamic work distribution
- `StringBuilder` — efficient string construction for the synthetic text
- `(int)Math.Sqrt(Limit)` — phase-1 sequential bound

## How to Run

### Prerequisites
- .NET 8 SDK

### Steps
```bash
cd Lab7/csharp
dotnet run
```
