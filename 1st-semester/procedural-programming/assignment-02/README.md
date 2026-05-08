# Assignment 02

Two exercises covering arrays, sentinels, and file-based record processing.

## Course
Procedural Programming — Semester 1

## Language
C++17 (migrated from C)

## Exercises

| File | Description |
|------|-------------|
| `ex06_min_max_array.cpp` | Reads integers until -1 sentinel; reports min and max |
| `ex09_student_absences.cpp` | Reads a student CSV; writes a report of students with > 100 absences |

## How to Build

```bash
cmake -S . -B build
cmake --build build
```

## What It Demonstrates
- `std::vector` replacing C-style arrays with sentinel loops
- `std::minmax_element` from `<algorithm>`
- `std::fstream` replacing `FILE*` for file I/O
- `std::getline` replacing unsafe `gets()`
- RAII resource management — no manual `fclose()`
