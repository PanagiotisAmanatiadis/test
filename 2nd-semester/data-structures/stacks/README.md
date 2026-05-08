# Stacks

Two array stack exercises covering top-element retrieval and stack-to-stack transfers.

## Course
Data Structures — Semester 2

## Language
C++17 (migrated from C)

## Exercises

| File | Description |
|------|-------------|
| `stack_int_top.cpp` | Integer stack (limit 50); pushes odd numbers 1–99; demonstrates `GetTopElementA` (empty-guarded, returns `std::optional<int>`) and `GetTopElementB` (direct access) |
| `stack_char_copy.cpp` | Character stack (limit 6); loads "PASCAL"; copies chain Stack1 → Stack2 → Stack3 → Stack1 |

## How to Build

```bash
cmake -S . -B build
cmake --build build
```

## What It Demonstrates
- Fixed-size array stack with push, pop, and peek operations
- Safe top access via `std::optional<int>` vs. direct index access
- Stack-to-stack element migration preserving LIFO semantics
- `[[nodiscard]]` on query functions; `std::underflow_error` for empty-stack guards
- Native `bool` replacing C `boolean` enum
