/**
 * @file stack_int_top.cpp
 * @brief Array stack of integers — two GetTopElement implementations.
 *
 * Pushes all odd numbers from 1 to 99 onto a stack (limit 50), then
 * retrieves the top element using two different methods:
 *   - GetTopElementA: checks for empty before access
 *   - GetTopElementB: direct index access (assumes non-empty)
 */

#include <array>
#include <iostream>
#include <optional>
#include <stdexcept>

namespace {
    constexpr int STACK_LIMIT = 50;
}

/** @brief Fixed-size array stack of integers. */
struct Stack {
    int top{-1};
    std::array<int, STACK_LIMIT> elements{};

    [[nodiscard]] bool empty() const { return top == -1; }
    [[nodiscard]] bool full()  const { return top == STACK_LIMIT - 1; }
};

void push(Stack& s, int item) {
    if (s.full()) { std::cout << "Full stack.\n"; return; }
    s.elements[++s.top] = item;
}

[[nodiscard]] int pop(Stack& s) {
    if (s.empty()) throw std::underflow_error("Empty stack");
    return s.elements[s.top--];
}

// ── Top-element strategies ───────────────────────────────────────────────────

/**
 * @brief Return the top element only when the stack is non-empty.
 * @return The top value, or std::nullopt if the stack is empty.
 */
[[nodiscard]] std::optional<int> getTopElementA(const Stack& s) {
    if (!s.empty())
        return s.elements[s.top];
    return std::nullopt;
}

/**
 * @brief Return the top element by direct index (caller must ensure non-empty).
 * @throws std::underflow_error if the stack is empty.
 */
[[nodiscard]] int getTopElementB(const Stack& s) {
    if (s.empty()) throw std::underflow_error("Empty stack");
    return s.elements[s.top];
}

// ── Entry point ──────────────────────────────────────────────────────────────

int main() {
    Stack s;

    for (int i = 1; i <= 99; i += 2)
        push(s, i);

    if (auto topA = getTopElementA(s))
        std::cout << "TopA = " << *topA << '\n';
    else
        std::cout << "TopA: stack is empty.\n";

    std::cout << "TopB = " << getTopElementB(s) << '\n';

    return 0;
}
