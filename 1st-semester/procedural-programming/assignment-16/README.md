# Assignment 16

Three exercises covering tiered pricing, array search, and character classification.

## Course
Procedural Programming — Semester 1

## Language
C++17 (migrated from C)

## Exercises

| File | Description |
|------|-------------|
| `ex02_sms_cost.cpp` | Computes SMS bill using a four-tier pricing structure |
| `ex05_array_occurrences.cpp` | Finds all positions of a digit in a random 50-element array |
| `ex07_digit_sum.cpp` | Sums digit characters in an alphanumeric string with formatted output |

## How to Build

```bash
cmake -S . -B build
cmake --build build
```

## What It Demonstrates
- `[[nodiscard]]` tiered-cost pure function
- `std::vector<int>` for dynamic occurrence tracking replacing a C array
- Range-based for loops with `std::isdigit` from `<cctype>`
- `std::getline` replacing `gets()`
