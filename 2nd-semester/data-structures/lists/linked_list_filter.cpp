/**
 * @file linked_list_filter.cpp
 * @brief Pointer-based singly linked list — demonstrates Larger (filter).
 *
 * Reads N integers into a source list, then builds a new output list that
 * contains only the elements greater than or equal to a given threshold,
 * preserving source order.
 */

#include <iostream>

/** @brief Node in a pointer-based singly linked list. */
struct ListNode {
    int       data{};
    ListNode* next{nullptr};
};

// ── Helpers ──────────────────────────────────────────────────────────────────

[[nodiscard]] bool isEmpty(const ListNode* list) { return list == nullptr; }

void linkedInsert(ListNode*& list, int item, ListNode* predPtr) {
    auto* tmp = new ListNode{item, nullptr};
    if (predPtr == nullptr) {
        tmp->next = list;
        list      = tmp;
    } else {
        tmp->next      = predPtr->next;
        predPtr->next  = tmp;
    }
}

void linkedTraverse(const ListNode* list) {
    if (isEmpty(list)) {
        std::cout << "Empty list.\n";
        return;
    }
    for (const ListNode* cur = list; cur != nullptr; cur = cur->next)
        std::cout << cur->data << ", ";
    std::cout << '\n';
}

/** @brief Free every node in the list. */
void deleteAll(ListNode*& list) {
    while (!isEmpty(list)) {
        ListNode* tmp = list;
        list = list->next;
        delete tmp;
    }
}

// ── Feature ──────────────────────────────────────────────────────────────────

/**
 * @brief Build a new list of all elements in @p src that are >= @p threshold,
 *        in the same relative order as they appear in @p src.
 * @return Pointer to the head of the new filtered list (caller owns memory).
 */
[[nodiscard]] ListNode* larger(const ListNode* src, int threshold) {
    ListNode* outList{nullptr};
    ListNode* tail{nullptr};          // tracks insertion point to preserve order

    for (const ListNode* cur = src; cur != nullptr; cur = cur->next) {
        if (cur->data >= threshold) {
            linkedInsert(outList, cur->data, tail);
            // advance tail to the newly appended node
            tail = (tail == nullptr) ? outList : tail->next;
        }
    }
    return outList;
}

// ── Entry point ──────────────────────────────────────────────────────────────

int main() {
    ListNode* list{nullptr};

    int n{};
    std::cout << "Number of elements: ";
    std::cin >> n;

    for (int i = 0; i < n; ++i) {
        int val{};
        std::cout << "Value " << i + 1 << ": ";
        std::cin >> val;
        linkedInsert(list, val, nullptr);
    }

    std::cout << "Source list:        ";
    linkedTraverse(list);

    int threshold{};
    std::cout << "Threshold (>=): ";
    std::cin >> threshold;

    ListNode* filtered = larger(list, threshold);
    std::cout << "Filtered list:      ";
    linkedTraverse(filtered);

    deleteAll(list);
    deleteAll(filtered);
    return 0;
}
