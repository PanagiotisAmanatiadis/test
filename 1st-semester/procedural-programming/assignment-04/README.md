# Assignment 04

Three exercises covering structs, 2-D arrays, and file-based reporting.

## Course
Procedural Programming — Semester 1

## Language
C++17 (migrated from C)

## Exercises

| File | Description |
|------|-------------|
| `ex01_profit_calculator.cpp` | Computes profit and sale amount from purchase price and rate |
| `ex05_sales_report.cpp` | Reports income, commission, and unit sales for 4 salesmen × 5 products |
| `ex09_kickback_report.cpp` | Reads `i4f9.dat`; writes kickback amounts per product to `o4f9.dat` |

## How to Build

```bash
cmake -S . -B build
cmake --build build
```

## What It Demonstrates
- Aggregate return via `struct` (ProfitResult)
- `std::array` with `constexpr` data replacing C global arrays
- `std::fstream` + `std::getline` for CSV file I/O
- `switch`-based lookup table for rate mapping
