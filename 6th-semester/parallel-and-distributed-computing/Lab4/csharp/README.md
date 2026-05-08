# Lab 4 — Producer-Consumer & CarPark Simulation

Demonstrates condition synchronisation: blocking on an empty or full queue
and controlling concurrent access to a bounded resource.

## Course
Parallel and Distributed Computing — Semester 6

## Language
C# 12 / .NET 8

## Exercises

### Exercise 1 — Producer-Consumer

| Role | Behaviour |
|------|-----------|
| **Producer** | Enqueues 20 messages with increasing delays (0–19 ms); marks queue complete when done |
| **Consumer** | Dequeues each message with a 10 ms processing delay; exits when queue is drained |

`BlockingCollection<T>` (capacity 10) provides built-in back-pressure:
- `Add()` blocks when the queue is full
- `GetConsumingEnumerable()` blocks when empty and terminates after `CompleteAdding()`

### Exercise 2 — CarPark Simulation

20 cars attempt to enter a park with only 4 spaces.

```
Car arrives  →  SemaphoreSlim.Wait()  →  park (sleep)  →  SemaphoreSlim.Release()
```

- Cars arriving at a full park block automatically in `Wait()`
- A departing car calls `Release()`, unblocking one waiting car
- `_free` counter display is protected by a `lock` to prevent torn reads

## Key C# Synchronisation Primitives

| Primitive | Used for |
|-----------|----------|
| `BlockingCollection<T>` | Bounded producer-consumer queue with blocking add/take |
| `SemaphoreSlim(n,n)` | Limit concurrent access to n resources |
| `lock` | Atomic read-modify-print of the free-space counter |
| `GetConsumingEnumerable()` | Consumer loop that auto-exits when producer is done |

## How to Run

### Prerequisites
- .NET 8 SDK

### Steps
```bash
cd Lab4/csharp
dotnet run
```
