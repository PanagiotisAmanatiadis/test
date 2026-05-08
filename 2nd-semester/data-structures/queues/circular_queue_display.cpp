/**
 * @file circular_queue_display.cpp
 * @brief Circular array queue — two display strategies.
 *
 * Fills the queue with odd numbers 1–99, then demonstrates:
 *   - DisplayA: rotate-and-print (dequeue → print → re-enqueue)
 *   - DisplayB: direct index traversal without modifying the queue
 */

#include <array>
#include <iostream>
#include <stdexcept>

namespace {
    constexpr int QUEUE_LIMIT = 51;
}

/** @brief Circular array queue with a fixed capacity. */
struct Queue {
    int front{0};
    int rear{0};
    std::array<int, QUEUE_LIMIT> elements{};

    [[nodiscard]] bool empty() const { return front == rear; }
    [[nodiscard]] bool full()  const { return front == (rear + 1) % QUEUE_LIMIT; }
};

// ── Operations ───────────────────────────────────────────────────────────────

/** @brief Enqueue @p item. Prints a warning and discards if full. */
void addQ(Queue& q, int item) {
    if (q.full()) {
        std::cout << "Full queue — cannot enqueue " << item << ".\n";
        return;
    }
    q.elements[q.rear] = item;
    q.rear = (q.rear + 1) % QUEUE_LIMIT;
}

/**
 * @brief Dequeue and return the front item.
 * @throws std::underflow_error if queue is empty.
 */
[[nodiscard]] int removeQ(Queue& q) {
    if (q.empty()) throw std::underflow_error("Empty queue");
    int item  = q.elements[q.front];
    q.front   = (q.front + 1) % QUEUE_LIMIT;
    return item;
}

// ── Display strategies ───────────────────────────────────────────────────────

/**
 * @brief Rotate through the queue: dequeue each element, print it, re-enqueue.
 *        The queue contents are preserved after the call.
 */
void displayA(Queue& q) {
    int count = (q.rear - q.front + QUEUE_LIMIT) % QUEUE_LIMIT;
    for (int i = 0; i < count; ++i) {
        int item = removeQ(q);
        std::cout << item << '\n';
        addQ(q, item);
    }
}

/** @brief Traverse internal array by index — read-only, no side effects. */
void displayB(const Queue& q) {
    int cur = q.front;
    while (cur != q.rear) {
        std::cout << q.elements[cur] << '\n';
        cur = (cur + 1) % QUEUE_LIMIT;
    }
}

// ── Entry point ──────────────────────────────────────────────────────────────

int main() {
    Queue q;

    for (int i = 1; i <= 99; i += 2)
        addQ(q, i);

    std::cout << "--- DisplayA (rotate-and-print) ---\n";
    displayA(q);

    std::cout << "\n--- DisplayB (index traverse) ---\n";
    displayB(q);

    return 0;
}
