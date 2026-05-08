# Binary Trees

Two BST exercises covering recursive depth calculation and multi-tree employee management.

## Course
Data Structures — Semester 2

## Language
C++17 (migrated from C)

## Exercises

| File | Description |
|------|-------------|
| `bst_depth.cpp` | BST of `char`; inserts "PROCEDURE" and computes tree depth with `bstDepth()` using `std::max` |
| `bst_employee.cpp` | Three BSTs of employee records keyed by surname, partitioned by department code; file input from `I13F5.txt`; menu: build, insert, search, in-order print |

## How to Build

```bash
cmake -S . -B build
cmake --build build
```

## What It Demonstrates
- Recursive BST insert, search, and in-order traversal
- `std::unique_ptr<BSTNode>` replacing raw `malloc`/`free` — automatic memory management
- `std::string` replacing `char[]`; `std::ifstream` replacing `FILE*`
- `std::max` for depth calculation
- `[[nodiscard]]` on query functions; `nullptr` replacing `NULL`
- Native `bool` replacing C `boolean` enum; `fflush(stdin)` and `system("pause")` removed
