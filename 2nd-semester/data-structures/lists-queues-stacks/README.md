# Lists, Queues & Stacks (Combined)

Two exercises that combine linked data structures for real-world scenarios.

## Course
Data Structures — Semester 2

## Language
C++17 (migrated from C)

## Exercises

| File | Description |
|------|-------------|
| `login_queue.cpp` | Linked queue of active sessions; validates each username against a whitelist file (`I11f4.dat`) and prevents duplicate concurrent logins |
| `truck_loading_stack.cpp` | Linked stack for ordered truck loading (max 10 tonnes, value >= weight×300); inserts new items in descending weight order using a temporary stack |

## How to Build

```bash
cmake -S . -B build
cmake --build build
```

## What It Demonstrates
- Linked queue (front/rear pointers) with enqueue, dequeue, and linear search
- `std::ifstream` replacing `FILE*`/`fopen` for whitelist file reading
- Linked stack with ordered insertion using a temporary auxiliary stack
- `new`/`delete` replacing `malloc`/`free`; `nullptr` replacing `NULL`
- `[[nodiscard]]` on predicate and query functions
- Native `bool` replacing C `boolean` enum; `fflush(stdin)` and `system("pause")` removed
