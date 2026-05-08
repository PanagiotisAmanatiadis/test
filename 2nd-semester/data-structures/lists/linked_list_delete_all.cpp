/**
 * @file linked_list_delete_all.cpp
 * @brief Pointer-based singly linked list — demonstrates DeleteAll.
 *
 * Reads N integers, inserts each at the front of the list, displays the list,
 * then removes every node via DeleteAll and displays the empty list.
 */

#include <iostream>
#include <memory>

/** @brief Node in a pointer-based singly linked list. */
struct ListNode {
    int       data{};
    ListNode* next{nullptr};
};

// ── Helpers ──────────────────────────────────────────────────────────────────

[[nodiscard]] bool isEmpty(const ListNode* list) { return list == nullptr; }

/**
 * @brief Insert @p item before the node pointed to by @p predPtr
 *        (nullptr = insert at front).
 */
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

/** @brief Delete the node after @p predPtr (nullptr = delete head). */
void linkedDelete(ListNode*& list, ListNode* predPtr) {
    if (isEmpty(list)) {
        std::cout << "Empty list.\n";
        return;
    }
    ListNode* tmp{};
    if (predPtr == nullptr) {
        tmp   = list;
        list  = tmp->next;
    } else {
        tmp           = predPtr->next;
        predPtr->next = tmp->next;
    }
    delete tmp;
}

/** @brief Print every node value. */
void linkedTraverse(const ListNode* list) {
    if (isEmpty(list)) {
        std::cout << "Empty list.\n";
        return;
    }
    for (const ListNode* cur = list; cur != nullptr; cur = cur->next)
        std::cout << cur->data << ", ";
    std::cout << '\n';
}

// ── Feature ──────────────────────────────────────────────────────────────────

/** @brief Remove all nodes from the list. */
void deleteAll(ListNode*& list) {
    while (!isEmpty(list))
        linkedDelete(list, nullptr);
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

    std::cout << "Initial list:  ";
    linkedTraverse(list);

    deleteAll(list);

    std::cout << "After DeleteAll: ";
    linkedTraverse(list);

    return 0;
}
