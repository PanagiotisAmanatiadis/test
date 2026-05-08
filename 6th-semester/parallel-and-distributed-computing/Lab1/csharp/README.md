# Lab 1 — Introduction to Threads

Introduction to multi-threading in C#: creating threads, thread arrays, `Join()`,
polymorphism across worker classes, and observing non-deterministic concurrent output.

## Course
Parallel and Distributed Computing — Semester 6

## Language
C# 12 / .NET 8

## Exercises

| # | Description |
|---|-------------|
| Q1 | **Join without references** — without storing `Thread` objects you cannot call `Join()`. The main thread may exit before workers finish. |
| Q2 | **Two thread classes** — `GreeterWorker` and `CounterWorker` both implement `IWorker`, demonstrating polymorphism across two distinct constructors and `Execute()` bodies. |
| Q3 | **Ten threads each** — 10 instances of `GreeterWorker` and 10 of `CounterWorker` run concurrently (20 threads total). |
| Q4 | **Multiples calculator** — 10 threads each print the first 20 multiples of integers 1–10. Isolated: each thread's output is ordered. Concurrent: output interleaves non-deterministically. |

## How to Run

### Prerequisites
- .NET 8 SDK

### Steps
```bash
cd Lab1/csharp
dotnet run
```

## Project Structure
```
csharp/
├── src/
│   ├── IWorker.cs           # Shared interface enabling polymorphism
│   ├── GreeterWorker.cs     # Thread type A: prints greeting + thread id
│   ├── CounterWorker.cs     # Thread type B: counts from 1 to limit
│   ├── MultiplesWorker.cs   # Exercise 4 worker: prints multiples
│   └── Program.cs           # Runs all exercises in sequence
└── Lab1.csproj
```

## Key C# Threading Concepts
- `new Thread(method)` — create a thread pointing to an instance method
- `thread.Start()` — schedule the thread for execution
- `thread.Join()` — block caller until the thread terminates
- `Environment.CurrentManagedThreadId` — identify the running thread
