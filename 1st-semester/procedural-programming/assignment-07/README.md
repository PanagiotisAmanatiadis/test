# Assignment 07

Three exercises covering branching payroll logic, struct collections, and character-level file I/O.

## Course
Procedural Programming — Semester 1

## Language
C++17 (migrated from C)

## Exercises

| File | Description |
|------|-------------|
| `ex02_weekly_salary.cpp` | Weekly pay: hourly (with overtime) or annual ÷ 52 based on employee code |
| `ex08_car_rental.cpp` | Car rental records — tabular report, grand total, and highest-value rental |
| `ex09_extract_digits.cpp` | Reads `i7f9.dat`; writes contiguous digit sequences to `o7f9.dat` |

## How to Build

```bash
cmake -S . -B build
cmake --build build
```

## What It Demonstrates
- `CarRental` struct with a `[[nodiscard]] totalPrice()` const method
- `std::max_element` with a lambda comparator
- `std::fstream` character-by-character I/O replacing `getc`/`putc`
- `std::getline` replacing `gets()` for string input
- `const` correctness and range-based for loops
