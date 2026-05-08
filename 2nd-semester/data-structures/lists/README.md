# Lists

Five singly linked list exercises covering both array-based (storage pool) and pointer-based implementations.

## Course
Data Structures — Semester 2

## Language
C++17 (migrated from C)

## Exercises

| File | Description |
|------|-------------|
| `linked_list_int.cpp` | Array-based storage pool (10 nodes); integer data; ordered insert/delete/search via menu |
| `linked_list_student.cpp` | Array-based storage pool (5 nodes); student {name, grade} data; front insert, predecessor-based delete |
| `linked_list_delete_all.cpp` | Pointer-based dynamic list; inserts N integers at front, then removes all nodes via `deleteAll` |
| `linked_list_delete_last.cpp` | Pointer-based dynamic list; inserts N integers at front, then removes the tail node |
| `linked_list_filter.cpp` | Pointer-based dynamic list; builds a new filtered list of elements `>= threshold` |

## How to Build

```bash
cmake -S . -B build
cmake --build build
```

## What It Demonstrates
- Array-based linked list with a storage pool (free-list allocation pattern)
- Pointer-based dynamic list using `new`/`delete`
- Ordered insert maintaining ascending sort order
- `deleteAll`, `deleteLast`, and `filter` (Larger) list operations
- `[[nodiscard]]` on query functions
- `nullptr` replacing `NULL`; native `bool` replacing C `boolean` enum
