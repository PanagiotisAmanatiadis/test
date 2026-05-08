# Assignment 13

Three exercises covering series computation, matrix transformation, and digit decomposition.

## Course
Procedural Programming — Semester 1

## Language
C++17 (migrated from C)

## Exercises

| File | Description |
|------|-------------|
| `ex03_harmonic_number.cpp` | Computes H_100 = 1 + 1/2 + ... + 1/100 |
| `ex05_random_matrix.cpp` | Random matrix; transforms each row by propagating its max to lower indices |
| `ex06_digit_analysis.cpp` | Reports digit count, average digit, and max digit of an integer |

## How to Build

```bash
cmake -S . -B build
cmake --build build
```

## What It Demonstrates
- `[[nodiscard]]` pure numeric functions replacing output-pointer pairs
- `std::max_element` with iterator arithmetic for in-place row transforms
- `std::vector<std::vector<int>>` replacing VLAs and `calloc`
- `DigitStats` aggregate struct as a clean return type
