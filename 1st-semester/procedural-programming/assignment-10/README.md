# Assignment 10

Two exercises covering formatted table output and character-level text transformation.

## Course
Procedural Programming — Semester 1

## Language
C++17 (migrated from C)

## Exercises

| File | Description |
|------|-------------|
| `ex03_multiplication_table.cpp` | Prints a formatted 10×10 multiplication table |
| `ex09_space_after_punct.cpp` | Inserts a space after every `.` or `,` in a text file |

## How to Build

```bash
cmake -S . -B build
cmake --build build
```

## What It Demonstrates
- `std::setw` for aligned tabular output replacing `printf` format strings
- `std::fstream` character-by-character I/O with a boolean state flag
