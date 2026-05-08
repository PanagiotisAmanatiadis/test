# Assignment 20

Three exercises covering lookup tables, min/max tracking, and array rotation.

## Course
Procedural Programming — Semester 1

## Language
C++17 (migrated from C)

## Exercises

| File | Description |
|------|-------------|
| `ex02_day_name.cpp` | Maps an integer [1–7] to a day name with bounds-checked exception |
| `ex03_age_min_max.cpp` | Reads ages until -1; reports min and max |
| `ex05_array_rotation.cpp` | Right-rotates a 5-element array by one position |

## How to Build

```bash
cmake -S . -B build
cmake --build build
```

## What It Demonstrates
- `constexpr std::array<std::string_view>` lookup table replacing C char* array
- `std::out_of_range` replacing `assert()` for bounds checking
- `std::rotate` on reverse iterators replacing `memmove`
- Sentinel loop with idiomatic comma-operator condition
