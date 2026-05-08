# Assignment 09

Three exercises covering discount tiers, sales aggregation, and payroll computation.

## Course
Procedural Programming — Semester 1

## Language
C++17 (migrated from C)

## Exercises

| File | Description |
|------|-------------|
| `ex02_product_discount.cpp` | Derives price from product code; applies quantity-tier discount |
| `ex06_sales_analysis.cpp` | Reports revenue and units per salesman/product; highlights best performers |
| `ex08_teacher_salary.cpp` | Reads N teachers; computes and prints gross, deductions, tax, and net pay |

## How to Build

```bash
cmake -S . -B build
cmake --build build
```

## What It Demonstrates
- `class Box` / `struct Teacher` with encapsulated computation methods
- `std::max_element` with iterator arithmetic for best-index lookup
- `constexpr std::array` replacing C global arrays
- `std::getline` + `std::cin.ignore()` for mixed numeric/string input
- Template function for generic best-of reporting
