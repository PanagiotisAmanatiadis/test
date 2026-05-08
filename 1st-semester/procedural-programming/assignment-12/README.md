# Assignment 12

Property tax calculator using area-based formulas.

## Course
Procedural Programming — Semester 1

## Language
C++17 (migrated from C)

## Exercises

| File | Description |
|------|-------------|
| `ex01_property_tax.cpp` | Computes transfer tax (DT) and stamp duty (DF) from net and gross area |

## How to Build

```bash
cmake -S . -B build
cmake --build build
```

## What It Demonstrates
- `constexpr` named constant replacing a macro
- Aggregate `PropertyTax` struct returned by a `[[nodiscard]]` pure function
