# Hash

Hash table with chaining (synonym lists) for user record management.

## Course
Data Structures — Semester 2

## Language
C++17 (migrated from C)

## Exercises

| File | Description |
|------|-------------|
| `hash_table_chaining.cpp` | Static hash table (HMax=10, VMax=30); each bucket heads a synonym chain within a flat `std::array`; supports insert, delete, search, and full listing via menu |

## How to Build

```bash
cmake -S . -B build
cmake --build build
```

## What It Demonstrates
- Hash table with chaining using a flat array and a free-list stack for slot allocation
- `hashKey` function (key % HMax) for bucket selection
- Synonym-list search and predecessor tracking for O(1) delete
- `std::array` replacing C arrays; `std::string` replacing `char[]`
- `[[nodiscard]]` on predicate and lookup functions
- Native `bool` replacing C `boolean` enum; `fflush(stdin)` and `system("pause")` removed
