# Assignment 08

Box geometry calculator: surface area and volume from three dimensions.

## Course
Procedural Programming — Semester 1

## Language
C++17 (migrated from C)

## Exercises

| File | Description |
|------|-------------|
| `ex08_box_calculator.cpp` | Reads width, height, depth; reports surface area and volume |

## How to Build

```bash
cmake -S . -B build
cmake --build build
```

## What It Demonstrates
- C `struct` converted to a `class` with private data and `const` member methods
- `[[nodiscard]]` on pure geometry methods
