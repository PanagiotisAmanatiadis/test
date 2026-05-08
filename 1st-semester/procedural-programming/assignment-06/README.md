# Assignment 06

Two exercises covering arithmetic computations and multi-field statistical grouping.

## Course
Procedural Programming — Semester 1

## Language
C++17 (migrated from C)

## Exercises

| File | Description |
|------|-------------|
| `ex01_gift_bonus.cpp` | Computes annual bonus = days × wage × rate |
| `ex06_gender_averages.cpp` | Reads N people; reports average weight, height, and age by gender |

## How to Build

```bash
cmake -S . -B build
cmake --build build
```

## What It Demonstrates
- `[[nodiscard]]` pure functions replacing void output-pointer patterns
- `std::array` for fixed-size accumulators
- Range-based for loops over `std::vector<Person>`
- `const` correctness throughout
