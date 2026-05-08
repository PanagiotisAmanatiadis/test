/**
 * @file stack_char_copy.cpp
 * @brief Array stack of characters — copy chain Stack1 → Stack2 → Stack3 → Stack1.
 *
 * Pushes the characters of "PASCAL" onto Stack1, then transfers them through
 * three stacks to demonstrate stack-to-stack element migration, printing the
 * contents of each stack after every transfer step.
 */

#include <array>
#include <iostream>
#include <stdexcept>

namespace {
    constexpr int STACK_LIMIT = 6;
}

/** @brief Fixed-size array stack of characters. */
struct Stack {
    int  top{-1};
    std::array<char, STACK_LIMIT> elements{};

    [[nodiscard]] bool empty() const { return top == -1; }
    [[nodiscard]] bool full()  const { return top == STACK_LIMIT - 1; }
    [[nodiscard]] char peek()  const { return elements[top]; }
};

void push(Stack& s, char item) {
    if (s.full()) { std::cout << "Full stack.\n"; return; }
    s.elements[++s.top] = item;
}

[[nodiscard]] char pop(Stack& s) {
    if (s.empty()) throw std::underflow_error("Empty stack");
    return s.elements[s.top--];
}

void traverseStack(const Stack& s) {
    std::cout << "Size: " << s.top + 1 << '\n';
    for (int i = 0; i <= s.top; ++i)
        std::cout << s.elements[i] << ", ";
    std::cout << '\n';
}

// ── Entry point ──────────────────────────────────────────────────────────────

int main() {
    Stack stack1, stack2, stack3;

    // Load "PASCAL" onto Stack1.
    for (char c : {'P', 'A', 'S', 'C', 'A', 'L'})
        push(stack1, c);

    std::cout << "Stack1 (initial):\n";
    traverseStack(stack1);

    // Stack1 → Stack2
    while (!stack1.empty())
        push(stack2, pop(stack1));

    std::cout << "\nStack2 (after Stack1 → Stack2):\n";
    traverseStack(stack2);

    // Stack2 → Stack3
    while (!stack2.empty())
        push(stack3, pop(stack2));

    std::cout << "\nStack3 (after Stack2 → Stack3):\n";
    traverseStack(stack3);

    // Stack3 → Stack1
    while (!stack3.empty()) {
        push(stack1, stack3.peek());
        pop(stack3);
    }

    std::cout << "\nStack1 (after Stack3 → Stack1):\n";
    traverseStack(stack1);

    return 0;
}
