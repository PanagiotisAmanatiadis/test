/**
 * @file queue_reverse.cpp
 * @brief Circular array queue + array stack — reverses queue contents.
 *
 * Fills the queue with even numbers 2–30, prints the original order,
 * reverses it using an intermediate stack, then prints the reversed order.
 */

#include <array>
#include <iostream>
#include <stdexcept>

namespace {
    constexpr int QUEUE_LIMIT = 16;
    constexpr int STACK_LIMIT = 16;
}

// ── Queue ────────────────────────────────────────────────────────────────────

/** @brief Circular array queue. */
struct Queue {
    int front{0};
    int rear{0};
    std::array<int, QUEUE_LIMIT> elements{};

    [[nodiscard]] bool empty() const { return front == rear; }
    [[nodiscard]] bool full()  const { return front == (rear + 1) % QUEUE_LIMIT; }
};

void addQ(Queue& q, int item) {
    if (q.full()) { std::cout << "Full queue.\n"; return; }
    q.elements[q.rear] = item;
    q.rear = (q.rear + 1) % QUEUE_LIMIT;
}

[[nodiscard]] int removeQ(Queue& q) {
    if (q.empty()) throw std::underflow_error("Empty queue");
    int item = q.elements[q.front];
    q.front  = (q.front + 1) % QUEUE_LIMIT;
    return item;
}

void traverseQ(const Queue& q) {
    int cur = q.front;
    while (cur != q.rear) {
        std::cout << q.elements[cur] << '\n';
        cur = (cur + 1) % QUEUE_LIMIT;
    }
}

// ── Stack ────────────────────────────────────────────────────────────────────

/** @brief Fixed-size array stack. */
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

// ── Feature ──────────────────────────────────────────────────────────────────

/**
 * @brief Reverse the order of all elements in @p q using an auxiliary stack.
 */
void reverseQ(Queue& q) {
    Stack s;
    while (!q.empty())
        push(s, removeQ(q));
    while (!s.empty())
        addQ(q, pop(s));
}

// ── Entry point ──────────────────────────────────────────────────────────────

int main() {
    Queue q;

    for (int i = 2; i <= 30; i += 2)
        addQ(q, i);

    std::cout << "--- Original queue ---\n";
    traverseQ(q);

    reverseQ(q);

    std::cout << "\n--- Reversed queue ---\n";
    traverseQ(q);

    return 0;
}
