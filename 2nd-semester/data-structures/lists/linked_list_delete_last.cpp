/**
 * @file linked_list_delete_last.cpp
 * @brief Pointer-based singly linked list — demonstrates DeleteLast.
 *
 * Reads N integers, inserts each at the front of the list, displays the list,
 * removes the last (tail) node, then displays the updated list.
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

void linkedDelete(ListNode*& list, ListNode* predPtr) {
    if (isEmpty(list)) {
        std::cout << "Empty list.\n";
        return;
    }
    ListNode* tmp{};
    if (predPtr == nullptr) {
        tmp  = list;
        list = tmp->next;
    } else {
        tmp           = predPtr->next;
        predPtr->next = tmp->next;
    }
    delete tmp;
}

/** @brief Linear search: sets @p predPtr to the predecessor of @p item.
 *  @param[out] predPtr  Predecessor node, nullptr if item is the head.
 *  @param[out] found    True when item exists.
 */
void linearSearch(ListNode* list, int item,
                  ListNode*& predPtr, bool& found)
{
    predPtr = nullptr;
    found   = false;
    for (ListNode* cur = list; cur != nullptr; cur = cur->next) {
        if (cur->data == item) {
            found = true;
            return;
        }
        predPtr = cur;
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

// ── Feature ──────────────────────────────────────────────────────────────────

/** @brief Remove the tail node from the list. */
void deleteLastElement(ListNode*& list) {
    if (isEmpty(list)) {
        std::cout << "Empty list.\n";
        return;
    }
    // Walk to the last node.
    ListNode* cur = list;
    while (cur->next != nullptr)
        cur = cur->next;

    ListNode* pred{nullptr};
    bool      found{false};
    linearSearch(list, cur->data, pred, found);
    linkedDelete(list, pred);
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

    std::cout << "Initial list:      ";
    linkedTraverse(list);

    deleteLastElement(list);

    std::cout << "After DeleteLast:  ";
    linkedTraverse(list);

    return 0;
}
