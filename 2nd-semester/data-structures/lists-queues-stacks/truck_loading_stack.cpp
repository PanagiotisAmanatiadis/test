/**
 * @file truck_loading_stack.cpp
 * @brief Linked stack — ordered truck loading with weight and value constraints.
 *
 * A truck's platform is modelled as a linked stack of cargo weights (floats).
 * The platform is pre-loaded with weights [3, 2, 1, 0.5, 0.4] (bottom→top).
 * Total capacity is 10 tonnes; cost per tonne is 300.
 *
 * For each new item the user enters:
 *   - Weight > 0 and value >= weight×300 are required.
 *   - Total weight after loading must not exceed 10.
 *   - Items are inserted in descending weight order (heaviest at the bottom).
 *
 * Input ends when weight <= 0 or value <= 0.
 */

#include <iostream>
#include <iomanip>

/** @brief Node in a pointer-based singly linked stack. */
struct StackNode {
    float      data{};
    StackNode* next{nullptr};
};

/** @brief Linked stack (top is the head of the list). */
struct Stack {
    StackNode* top{nullptr};
    [[nodiscard]] bool empty() const { return top == nullptr; }
    [[nodiscard]] float peek() const { return top->data; }
};

// ── Stack operations ──────────────────────────────────────────────────────────

void push(Stack& s, float item) {
    auto* node = new StackNode{item, s.top};
    s.top = node;
}

[[nodiscard]] float pop(Stack& s) {
    if (s.empty()) return 0.0f;
    float val = s.top->data;
    StackNode* tmp = s.top;
    s.top = s.top->next;
    delete tmp;
    return val;
}

void traverseStack(const Stack& s) {
    if (s.empty()) { std::cout << "  (empty)\n"; return; }
    for (const StackNode* cur = s.top; cur != nullptr; cur = cur->next)
        std::cout << "  " << std::fixed << std::setprecision(1) << cur->data << '\n';
}

// ── Domain logic ──────────────────────────────────────────────────────────────

/**
 * @brief Insert @p weight into @p truckStack in descending order.
 *        Items lighter than @p weight are temporarily moved to @p tempStack.
 */
void insertOrdered(Stack& truckStack, Stack& tempStack, float weight) {
    // Pop items lighter than the new weight into tempStack.
    while (!truckStack.empty() && truckStack.peek() < weight)
        push(tempStack, pop(truckStack));

    push(truckStack, weight);

    std::cout << "-- Platform --\n";
    traverseStack(tempStack);
    std::cout << "-- Truck --\n";
    traverseStack(truckStack);

    // Restore lighter items on top.
    while (!tempStack.empty())
        push(truckStack, pop(tempStack));
}

// ── Entry point ───────────────────────────────────────────────────────────────

int main() {
    Stack truckStack, tempStack;

    // Pre-load: heaviest at bottom (push in ascending order so heaviest ends
    // up deepest in the linked stack).
    push(truckStack, 3.0f);
    push(truckStack, 2.0f);
    push(truckStack, 1.0f);
    push(truckStack, 0.5f);
    push(truckStack, 0.4f);

    float totalWeight = 6.9f;
    constexpr float MAX_WEIGHT   = 10.0f;
    constexpr float COST_PER_TON = 300.0f;

    while (true) {
        float weight{};
        std::cout << "Weight (<=0 to quit): ";
        std::cin >> weight;
        if (weight <= 0.0f) break;

        float value{};
        std::cout << "Value (<=0 to quit): ";
        std::cin >> value;
        if (value <= 0.0f) break;

        float cost = weight * COST_PER_TON;
        if (totalWeight + weight > MAX_WEIGHT || value < cost) {
            std::cout << "Rejected: ";
            if (totalWeight + weight > MAX_WEIGHT)
                std::cout << "exceeds capacity.\n";
            else
                std::cout << "insufficient value.\n";
            continue;
        }

        if (!truckStack.empty() && weight <= truckStack.peek()) {
            // Fits on top — weight is lighter than or equal to current top.
            push(truckStack, weight);
            std::cout << "-- Platform (empty) --\n-- Truck --\n";
            traverseStack(truckStack);
        } else {
            insertOrdered(truckStack, tempStack, weight);
        }
        totalWeight += weight;
    }

    std::cout << "\n-- Final Truck --\n";
    traverseStack(truckStack);

    return 0;
}
