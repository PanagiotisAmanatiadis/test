# Sets

Two boolean-array set ADT exercises covering membership validation and power set generation.

## Course
Data Structures — Semester 2

## Language
C++17 (migrated from C)

## Exercises

| File | Description |
|------|-------------|
| `set_validation.cpp` | Set of size 255 over ASCII codes; validates user input as integers (`[sign] digit+`) and identifiers (`(letter|_)(letter|digit|_)*`) using set membership |
| `set_power_set.cpp` | Set of size 6; generates all 64 subsets of the universe {1,2,3,4,5} via bitmask, stores them in a `std::vector<Set>`, prints odd-indexed subsets |

## How to Build

```bash
cmake -S . -B build
cmake --build build
```

## What It Demonstrates
- Boolean-array set representation (`std::array<bool, N>`)
- Set primitives: create, insert, remove, member
- Bitmask enumeration of a power set
- `std::vector` replacing VLA for dynamically-sized array of sets
- `[[nodiscard]]` on predicate functions; `static_cast<unsigned char>` for safe `ctype` usage
- Native `bool` replacing C `boolean` enum; `fflush(stdin)` removed
