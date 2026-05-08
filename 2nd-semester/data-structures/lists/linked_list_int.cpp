/**
 * @file linked_list_int.cpp
 * @brief Array-based linked list (storage pool) storing integers.
 *
 * Implements a singly linked list over a fixed-size storage pool of 10 nodes.
 * Supports ordered insert, delete, traverse, and linear search via a menu.
 */

#include <array>
#include <iostream>
#include <limits>

namespace {
    constexpr int  NUM_NODES = 10;
    constexpr int  NIL       = -1;
}

/** @brief One node in the storage pool. */
struct Node {
    int data{NIL};
    int next{NIL};
};

using Pool    = std::array<Node, NUM_NODES>;
using NodeIdx = int;

// ── Storage pool primitives ──────────────────────────────────────────────────

/** @brief Initialise every slot into a free-list chain. */
void initPool(Pool& pool, NodeIdx& freePtr) {
    for (int i = 0; i < NUM_NODES - 1; ++i) {
        pool[i].data = NIL;
        pool[i].next = i + 1;
    }
    pool[NUM_NODES - 1].data = NIL;
    pool[NUM_NODES - 1].next = NIL;
    freePtr = 0;
}

[[nodiscard]] bool isEmpty(NodeIdx list)    { return list == NIL; }
[[nodiscard]] bool isFull(NodeIdx freePtr)  { return freePtr == NIL; }

/** @brief Allocate one node from the free list; returns NIL if full. */
NodeIdx getNode(Pool& pool, NodeIdx& freePtr) {
    NodeIdx p = freePtr;
    if (!isFull(freePtr))
        freePtr = pool[freePtr].next;
    return p;
}

/** @brief Return a node back to the free list. */
void releaseNode(Pool& pool, NodeIdx p, NodeIdx& freePtr) {
    pool[p].next = freePtr;
    pool[p].data = NIL;
    freePtr = p;
}

// ── List operations ──────────────────────────────────────────────────────────

/**
 * @brief Ordered search: finds the predecessor of the position where @p item
 *        belongs (ascending order).
 * @param[out] predPtr  Index of predecessor, NIL if item goes at the front.
 * @param[out] found    True when item already exists in the list.
 */
void search(NodeIdx freePtr, NodeIdx list, const Pool& pool,
            int item, bool& found, NodeIdx& predPtr)
{
    found   = false;
    predPtr = NIL;

    if (isEmpty(list)) return;

    NodeIdx current = list;
    while (current != NIL) {
        if (pool[current].data >= item) {
            found = (pool[current].data == item);
            return;
        }
        predPtr = current;
        current = pool[current].next;
    }
}

/** @brief Insert @p item after the node at @p predPtr (NIL = insert at front). */
void insert(NodeIdx& list, Pool& pool, NodeIdx& freePtr,
            NodeIdx predPtr, int item)
{
    if (isFull(freePtr)) {
        std::cout << "Full list — cannot insert.\n";
        return;
    }
    NodeIdx tmp = getNode(pool, freePtr);
    pool[tmp].data = item;
    if (predPtr == NIL) {
        pool[tmp].next = list;
        list = tmp;
    } else {
        pool[tmp].next       = pool[predPtr].next;
        pool[predPtr].next   = tmp;
    }
}

/** @brief Delete the node that follows @p predPtr (NIL = delete head). */
void deleteNode(NodeIdx& list, Pool& pool, NodeIdx& freePtr, NodeIdx predPtr) {
    if (isEmpty(list)) {
        std::cout << "Empty list — nothing to delete.\n";
        return;
    }
    NodeIdx tmp;
    if (predPtr == NIL) {
        tmp  = list;
        list = pool[tmp].next;
    } else {
        tmp              = pool[predPtr].next;
        pool[predPtr].next = pool[tmp].next;
    }
    releaseNode(pool, tmp, freePtr);
}

/** @brief Print all active list nodes (index: data, next). */
void traverse(NodeIdx list, const Pool& pool) {
    if (isEmpty(list)) {
        std::cout << "Empty list.\n";
        return;
    }
    NodeIdx cur = list;
    while (cur != NIL) {
        std::cout << '(' << cur << ": " << pool[cur].data
                  << ", " << pool[cur].next << ") ";
        cur = pool[cur].next;
    }
    std::cout << '\n';
}

/** @brief Dump the raw storage pool (all slots). */
void printPool(NodeIdx list, NodeIdx freePtr, const Pool& pool) {
    std::cout << "Head=" << list << "  FreePtr=" << freePtr << '\n';
    for (int i = 0; i < NUM_NODES; ++i)
        std::cout << '(' << i << ": " << pool[i].data
                  << ", " << pool[i].next << ") ";
    std::cout << '\n';
}

// ── Menu ─────────────────────────────────────────────────────────────────────

int readChoice() {
    int c{};
    std::cout << "\n--- MENU ---\n"
              << "1. Create list\n"
              << "2. Insert element\n"
              << "3. Traverse list\n"
              << "4. Delete element\n"
              << "5. Is list empty?\n"
              << "6. Is list full?\n"
              << "7. Print storage pool\n"
              << "8. Search element\n"
              << "9. Quit\n"
              << "Choice: ";
    while (!(std::cin >> c) || c < 1 || c > 9) {
        std::cin.clear();
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
        std::cout << "Choice (1-9): ";
    }
    return c;
}

int main() {
    Pool    pool;
    NodeIdx freePtr{};
    NodeIdx list{NIL};

    initPool(pool, freePtr);
    printPool(list, freePtr, pool);

    int choice{};
    do {
        choice = readChoice();
        switch (choice) {
        case 1:
            list = NIL;
            std::cout << "List created (empty).\n";
            break;

        case 2: {
            char cont{'Y'};
            do {
                int item{};
                std::cout << "FreePtr=" << freePtr << "\nValue to insert: ";
                std::cin >> item;
                bool    found{};
                NodeIdx pred{NIL};
                search(freePtr, list, pool, item, found, pred);
                insert(list, pool, freePtr, pred, item);
                std::cout << "List head=" << list << "\nContinue? (Y/N): ";
                std::cin >> cont;
            } while (std::toupper(static_cast<unsigned char>(cont)) != 'N');
            printPool(list, freePtr, pool);
            break;
        }

        case 3:
            std::cout << "FreePtr=" << freePtr << '\n';
            traverse(list, pool);
            break;

        case 4:
            if (isEmpty(list)) {
                std::cout << "Empty list.\n";
            } else {
                printPool(list, freePtr, pool);
                int item{};
                std::cout << "Value to delete: ";
                std::cin >> item;
                bool    found{};
                NodeIdx pred{NIL};
                search(freePtr, list, pool, item, found, pred);
                if (found)
                    deleteNode(list, pool, freePtr, pred);
                else
                    std::cout << "Element not found.\n";
                printPool(list, freePtr, pool);
            }
            break;

        case 5:
            std::cout << (isEmpty(list) ? "List is empty." : "List is not empty.") << '\n';
            break;

        case 6:
            std::cout << (isFull(freePtr) ? "List is full." : "List is not full.") << '\n';
            break;

        case 7:
            printPool(list, freePtr, pool);
            break;

        case 8: {
            int item{};
            std::cout << "Value to search: ";
            std::cin >> item;
            bool    found{};
            NodeIdx pred{NIL};
            search(freePtr, list, pool, item, found, pred);
            if (found)
                std::cout << "Found; predecessor index: " << pred << '\n';
            else
                std::cout << "Not found.\n";
            break;
        }

        case 9:
            break;
        }
    } while (choice != 9);

    return 0;
}
