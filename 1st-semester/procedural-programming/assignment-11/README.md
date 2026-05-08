# Assignment 11

Three exercises covering 2-D numeric statistics and string parsing.

## Course
Procedural Programming — Semester 1

## Language
C++17 (migrated from C)

## Exercises

| File | Description |
|------|-------------|
| `ex05_temperature_data.cpp` | 10-city temperature averages and deviations (original logic preserved) |
| `ex05b_temperature_fixed.cpp` | Corrected version — max-deviation loop now iterates all samples per city |
| `ex07_email_parser.cpp` | Trims an email address and extracts local-part and domain |

## How to Build

```bash
cmake -S . -B build
cmake --build build
```

## What It Demonstrates
- `std::accumulate` replacing manual sum loops
- `std::fabs` from `<cmath>` replacing C `abs()` for doubles
- `std::string::find` and `substr` replacing C `strcspn` / pointer arithmetic
- Lambda-based `trim` using `std::find_if` on reverse iterators
- `[[nodiscard]]` pure functions for statistical computations
