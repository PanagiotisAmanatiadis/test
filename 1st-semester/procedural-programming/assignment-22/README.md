# Assignment 22

VAT calculator for a 5-product order with category-based tax rates.

## Course
Procedural Programming — Semester 1

## Language
C++17 (migrated from C)

## Exercises

| File | Description |
|------|-------------|
| `ex04_vat_calculator.cpp` | Reads 5 products; accumulates cost and VAT by category code |

## How to Build

```bash
cmake -S . -B build
cmake --build build
```

## What It Demonstrates
- `std::optional<float>` replacing an int-return sentinel for invalid input
- `switch`-based VAT rate lookup returning `std::nullopt` for invalid codes
- `[[nodiscard]]` on the rate mapping function
