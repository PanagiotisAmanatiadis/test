# Queues

Two circular array queue exercises demonstrating display strategies and queue reversal.

## Course
Data Structures — Semester 2

## Language
C++17 (migrated from C)

## Exercises

| File | Description |
|------|-------------|
| `circular_queue_display.cpp` | Circular queue (limit 51); fills with odd numbers 1–99; demonstrates rotate-and-print (DisplayA) and index-traverse (DisplayB) |
| `queue_reverse.cpp` | Circular queue + array stack (limit 16 each); fills with even numbers 2–30; reverses queue order via `reverseQ` using an auxiliary stack |

## How to Build

```bash
cmake -S . -B build
cmake --build build
```

## What It Demonstrates
- Circular array queue with modulo-wrap front/rear indices
- Two read strategies: destructive rotate-and-print vs. non-destructive index traversal
- Queue reversal using an intermediate array stack
- `[[nodiscard]]` on dequeue/pop; `std::underflow_error` for empty-container guards
- Native `bool` replacing C `boolean` enum
