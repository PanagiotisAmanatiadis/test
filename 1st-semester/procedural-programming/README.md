# Procedural Programming

A collection of programming exercises completed during the Procedural Programming
course in Semester 1. All exercises have been migrated from C to modern C++17.

## Course
Procedural Programming — Semester 1

## Language
C++17 (migrated from C)

## Prerequisites
- C++17-compatible compiler (GCC 9+, Clang 9+, MSVC 2019+)
- CMake 3.17+

## Assignment Overview

| Folder | Exercises | Topics |
|--------|-----------|--------|
| `assignment-02/` | ex06, ex09 | Sentinel arrays, CSV file I/O |
| `assignment-04/` | ex01, ex05, ex09 | Profit calculation, sales tables, file-based kickback report |
| `assignment-05/` | ex04, ex05 | Armstrong numbers, dynamic matrix sums |
| `assignment-06/` | ex01, ex06 | Bonus calculation, gender-grouped averages |
| `assignment-07/` | ex02, ex08, ex09 | Payroll, car rental records, digit extraction |
| `assignment-08/` | ex08 | Box geometry (area and volume) |
| `assignment-09/` | ex02, ex06, ex08 | Product discounts, sales analysis, teacher payroll |
| `assignment-10/` | ex03, ex09 | Multiplication table, space-after-punctuation transformer |
| `assignment-11/` | ex05, ex05b, ex07 | Temperature statistics (+ bugfix), email parser |
| `assignment-12/` | ex01 | Property transfer tax |
| `assignment-13/` | ex03, ex05, ex06 | Harmonic number, random matrix transform, digit analysis |
| `assignment-14/` | ex04, ex07 | Max formula, Fisher-Yates word shuffle |
| `assignment-16/` | ex02, ex05, ex07 | SMS cost tiers, array occurrences, digit sum |
| `assignment-17/` | ex04 | Arithmetic series sum (closed-form) |
| `assignment-20/` | ex02, ex03, ex05 | Day name lookup, age min/max, array rotation |
| `assignment-22/` | ex04 | VAT calculator with optional rate lookup |

## How to Build (per assignment)

```bash
cd assignment-XX
cmake -S . -B build
cmake --build build
```

## C → C++17 Migration Highlights

| C pattern | C++17 replacement |
|-----------|-------------------|
| `printf` / `scanf` | `std::cout` / `std::cin` |
| `gets()` | `std::getline()` |
| `FILE*` / `fopen` | `std::fstream` (RAII) |
| `malloc` / `calloc` / `free` | `std::vector` |
| C-style arrays | `std::array` / `std::vector` |
| `char*` strings | `std::string` / `std::string_view` |
| `struct` with free functions | `class` / `struct` with member methods |
| `assert()` for bounds | `std::out_of_range` exception |
| `rand()` + manual Fisher-Yates | `std::shuffle` + `std::mt19937` |
| `NULL` | `nullptr` |
| int-return sentinel | `std::optional<T>` |
| `#define` constants | `constexpr` named constants |

## Shared Utilities
- `include/Logger.hpp` — lightweight severity-levelled logger used for
  diagnostic output across all exercises
