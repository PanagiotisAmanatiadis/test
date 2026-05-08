# Assignment 05

Two exercises covering number theory and dynamic 2-D matrix operations.

## Course
Procedural Programming — Semester 1

## Language
C++17 (migrated from C)

## Exercises

| File | Description |
|------|-------------|
| `ex04_armstrong_numbers.cpp` | Prints all Armstrong numbers (sum of digit cubes) in [1, 999] |
| `ex05_matrix_sums.cpp` | Reads an m×n matrix; reports row sums, column sums, and diagonal sums |

## How to Build

```bash
cmake -S . -B build
cmake --build build
```

## What It Demonstrates
- Pure `[[nodiscard]]` predicate replacing a C `int` boolean
- `std::vector<std::vector<long>>` replacing `calloc`/pointer-arithmetic matrix
- Structured binding and range-based for loops
- RAII — no manual memory management
