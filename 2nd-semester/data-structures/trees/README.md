# Trees

Two BST exercises using iterative insert/delete and subject-based search.

## Course
Data Structures — Semester 2

## Language
C++17 (migrated from C)

## Exercises

| File | Description |
|------|-------------|
| `bst_random_generate.cpp` | BST of `char`; reads N, generates N random uppercase letters via `std::rand`, inserts iteratively (duplicates skipped), prints in-order |
| `bst_teacher.cpp` | BST of teacher records {name, number, code}; loaded from `I14F5.TXT` (CSV format); menu: build, insert, delete, search by name, search by subject code, in-order print |

## How to Build

```bash
cmake -S . -B build
cmake --build build
```

## What It Demonstrates
- Iterative BST insert, search (with and without parent tracking), and delete
- `BSTSearchBySubject`: full in-order traversal filtering by subject code
- `std::string` replacing `char[]`; `std::ifstream`/`std::getline` replacing `FILE*`/`fscanf`
- Manual memory management with `new`/`delete` and a recursive `destroyBST`
- `[[nodiscard]]` on search functions; `nullptr` replacing `NULL`
- Native `bool` replacing C `boolean` enum; `fflush(stdin)` and `system("pause")` removed
