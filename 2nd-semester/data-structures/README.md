# Data Structures

Twenty exercises covering fundamental data structures implemented in C++17,
migrated from the original C coursework.

## Course
Data Structures — Semester 2

## Language
C++17 (migrated from C)

## Topics

| Folder | Exercises | Key Concepts |
|--------|-----------|--------------|
| `lists/` | 5 | Array-based storage pool list, pointer-based dynamic list, DeleteAll, DeleteLast, Larger filter |
| `queues/` | 2 | Circular array queue, two display strategies, ReverseQ via stack |
| `stacks/` | 2 | Array stack, GetTopElement (safe/direct), stack-to-stack copy |
| `sets/` | 2 | Boolean-array set, integer/identifier validation, power set via bitmask |
| `hash/` | 1 | Hash table with chaining (synonym lists), CRUD menu |
| `lists-queues-stacks/` | 2 | Login queue with file auth, ordered truck-loading stack |
| `binary-trees/` | 2 | Recursive BST depth, employee BST partitioned by department |
| `trees/` | 2 | Iterative BST insert/delete, random generation, subject-code search |
| `huffman-binary-trees/` | 2 | Huffman decoding tree from code table, rightmost-path node count |

## How to Build

Each subfolder contains its own `CMakeLists.txt`:

```bash
cd <subfolder>
cmake -S . -B build
cmake --build build
```

## C → C++17 Migration Summary

| C pattern | C++17 replacement |
|-----------|-------------------|
| `malloc`/`free` | `new`/`delete` or `std::unique_ptr` |
| `char[]` strings | `std::string` |
| `FILE*`/`fopen` | `std::ifstream`/`std::ofstream` |
| `NULL` | `nullptr` |
| `bool` enum `{FALSE,TRUE}` | native `bool` |
| C arrays | `std::array` / `std::vector` |
| `fflush(stdin)` | removed |
| `system("pause")` | removed |
| `conio.h` | removed |
