# Assignment 14

Two exercises covering integer formulas and string randomisation.

## Course
Procedural Programming — Semester 1

## Language
C++17 (migrated from C)

## Exercises

| File | Description |
|------|-------------|
| `ex04_max_formula.cpp` | Computes Y = (2·max(a,b) + 3·greatest(a,b,c)) / 4 |
| `ex07_word_shuffler.cpp` | Returns a randomly shuffled copy of a word |

## How to Build

```bash
cmake -S . -B build
cmake --build build
```

## What It Demonstrates
- `std::max({a, b, c})` initialiser-list overload replacing a manual three-way comparison
- `std::shuffle` with `std::mt19937` replacing manual Fisher-Yates with `rand()`
- `std::random_device` for non-deterministic seeding
- `[[nodiscard]]` pure functions for both computations
