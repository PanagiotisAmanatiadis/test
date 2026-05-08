/**
 * @file linked_list_student.cpp
 * @brief Array-based linked list (storage pool) storing student records.
 *
 * Each node holds a student name and a grade (float).  The list uses a
 * fixed storage pool of 5 nodes.  Insertion is always at the front;
 * deletion is performed by specifying the predecessor's pool index.
 */

#include <array>
#include <iomanip>
#include <iostream>
#include <limits>
#include <string>

namespace {
    constexpr int  NUM_NODES = 5;
    constexpr int  NIL       = -1;
}

/** @brief Student record stored in each list node. */
struct Student {
    std::string name;
    float       grade{-1.0f};
};

/** @brief One node in the storage pool. */
struct Node {
    Student data;
    int     next{NIL};
};

using Pool    = std::array<Node, NUM_NODES>;
using NodeIdx = int;

// ── Storage pool primitives ──────────────────────────────────────────────────

void initPool(Pool& pool, NodeIdx& freePtr) {
    for (int i = 0; i < NUM_NODES - 1; ++i) {
        pool[i].data  = {" ", -1.0f};
        pool[i].next  = i + 1;
    }
    pool[NUM_NODES - 1].data = {" ", -1.0f};
    pool[NUM_NODES - 1].next = NIL;
    freePtr = 0;
}

[[nodiscard]] bool isEmpty(NodeIdx list)    { return list == NIL; }
[[nodiscard]] bool isFull(NodeIdx freePtr)  { return freePtr == NIL; }

NodeIdx getNode(Pool& pool, NodeIdx& freePtr) {
    NodeIdx p = freePtr;
    if (!isFull(freePtr))
        freePtr = pool[freePtr].next;
    return p;
}

void releaseNode(Pool& pool, NodeIdx p, NodeIdx& freePtr) {
    pool[p].data  = {" ", -1.0f};
    pool[p].next  = freePtr;
    freePtr = p;
}

// ── List operations ──────────────────────────────────────────────────────────

/** @brief Insert @p item after the node at @p predPtr (NIL = insert at front). */
void insert(NodeIdx& list, Pool& pool, NodeIdx& freePtr,
            NodeIdx predPtr, const Student& item)
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
        tmp                = pool[predPtr].next;
        pool[predPtr].next = pool[tmp].next;
    }
    releaseNode(pool, tmp, freePtr);
}

/** @brief Print active list nodes. */
void traverse(NodeIdx list, const Pool& pool) {
    if (isEmpty(list)) {
        std::cout << "Empty list.\n";
        return;
    }
    NodeIdx cur = list;
    while (cur != NIL) {
        std::cout << '(' << cur << ": " << pool[cur].data.name
                  << ", " << std::fixed << std::setprecision(2)
                  << pool[cur].data.grade
                  << ", " << pool[cur].next << ") ";
        cur = pool[cur].next;
    }
    std::cout << '\n';
}

/** @brief Dump all pool slots. */
void printPool(NodeIdx list, NodeIdx freePtr, const Pool& pool) {
    std::cout << "Head=" << list << "  FreePtr=" << freePtr << '\n';
    for (int i = 0; i < NUM_NODES; ++i)
        std::cout << '(' << i << ": " << pool[i].data.name
                  << ", " << std::fixed << std::setprecision(2)
                  << pool[i].data.grade
                  << ", " << pool[i].next << ") ";
    std::cout << '\n';
}

// ── Menu ─────────────────────────────────────────────────────────────────────

int readChoice() {
    int c{};
    std::cout << "\n--- MENU ---\n"
              << "1. Create list\n"
              << "2. Insert student\n"
              << "3. Traverse list\n"
              << "4. Delete student (by predecessor index)\n"
              << "5. Is list empty?\n"
              << "6. Is list full?\n"
              << "7. Print storage pool\n"
              << "8. Quit\n"
              << "Choice: ";
    while (!(std::cin >> c) || c < 1 || c > 8) {
        std::cin.clear();
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
        std::cout << "Choice (1-8): ";
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
                std::cout << "FreePtr=" << freePtr << '\n';
                Student s;
                std::cout << "Name: ";
                std::cin >> s.name;
                std::cout << "Grade: ";
                std::cin >> s.grade;
                insert(list, pool, freePtr, NIL, s);
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
                NodeIdx pred{};
                std::cout << "Predecessor index (-1 to delete head): ";
                std::cin >> pred;
                deleteNode(list, pool, freePtr, pred);
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

        case 8:
            break;
        }
    } while (choice != 8);

    return 0;
}
