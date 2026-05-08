# Huffman & Binary Trees

Two exercises: rightmost-path counting on a BST, and a Huffman decoding tree.

## Course
Data Structures — Semester 2

## Language
C++17 (migrated from C)

## Exercises

| File | Description |
|------|-------------|
| `bst_right_node_count.cpp` | BST of integers; reads values until -1; counts nodes on the rightmost path (root → rightmost leaf) via `rightNodeCount` |
| `huffman_decoder.cpp` | Builds a Huffman decoding tree from `codesRW.txt`, then decodes the bit stream in `program.txt` by traversing the tree |

## How to Build

```bash
cmake -S . -B build
cmake --build build
```

## What It Demonstrates
- Recursive rightmost-path count on a BST
- Huffman decoding tree construction: inserting symbols by following '0'/'1' code paths
- Leaf detection via `isLeaf()` method; decoding loop restarts from root at each leaf
- `std::unique_ptr<TreeNode>` replacing `malloc`/`free` — automatic memory management
- `std::ifstream` replacing `FILE*`; `std::string` replacing `char[]`
- `[[nodiscard]]` on query functions; `nullptr` replacing `NULL`
- Native `bool` replacing C `boolean` enum; `system("pause")` removed
