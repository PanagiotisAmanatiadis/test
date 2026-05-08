/**
 * @file login_queue.cpp
 * @brief Linked queue — user login system with file-based authentication.
 *
 * Reads user IDs from stdin, validates each against a whitelist file
 * (I11f4.dat), and prevents duplicate concurrent logins by checking whether
 * the ID is already in the active-sessions queue.
 */

#include <fstream>
#include <iostream>
#include <memory>
#include <string>

/** @brief Node in a pointer-based singly linked queue. */
struct QueueNode {
    std::string  userId;
    QueueNode*   next{nullptr};
};

/** @brief Linked queue with front/rear pointers. */
struct Queue {
    QueueNode* front{nullptr};
    QueueNode* rear{nullptr};

    [[nodiscard]] bool empty() const { return front == nullptr; }
};

// ── Queue operations ──────────────────────────────────────────────────────────

void enqueue(Queue& q, const std::string& item) {
    auto* node = new QueueNode{item, nullptr};
    if (q.front == nullptr)
        q.front = node;
    else
        q.rear->next = node;
    q.rear = node;
}

void dequeue(Queue& q, std::string& item) {
    if (q.empty()) { std::cout << "Empty queue.\n"; return; }
    QueueNode* tmp = q.front;
    item           = tmp->userId;
    q.front        = q.front->next;
    delete tmp;
    if (q.front == nullptr) q.rear = nullptr;
}

void traverseQueue(const Queue& q) {
    if (q.empty()) { std::cout << "Empty queue.\n"; return; }
    for (const QueueNode* cur = q.front; cur != nullptr; cur = cur->next)
        std::cout << cur->userId << ' ';
    std::cout << '\n';
}

// ── Domain logic ──────────────────────────────────────────────────────────────

/**
 * @brief Check whether @p userId exists in the whitelist file.
 * @param filename  Path to the whitelist (one userId per line).
 */
[[nodiscard]] bool isKnownUser(const std::string& filename,
                                const std::string& userId)
{
    std::ifstream file(filename);
    if (!file) {
        std::cout << "Cannot open file: " << filename << '\n';
        return false;
    }
    std::string line;
    while (file >> line)
        if (line == userId) return true;
    return false;
}

/** @brief Check whether @p userId is already in the active-sessions queue. */
[[nodiscard]] bool isAlreadyLoggedIn(const Queue& q, const std::string& userId) {
    for (const QueueNode* cur = q.front; cur != nullptr; cur = cur->next)
        if (cur->userId == userId) return true;
    return false;
}

// ── Entry point ───────────────────────────────────────────────────────────────

int main() {
    Queue sessions;
    char  cont{'Y'};

    do {
        std::string uid;
        std::cout << "Username: ";
        std::cin >> uid;

        if (!isKnownUser("I11f4.dat", uid)) {
            std::cout << "Wrong user ID.\n";
        } else if (isAlreadyLoggedIn(sessions, uid)) {
            std::cout << "Already logged in from another terminal — access denied.\n";
        } else {
            enqueue(sessions, uid);
        }

        std::cout << "New entry? (Y/N): ";
        std::cin >> cont;
        cont = static_cast<char>(std::toupper(static_cast<unsigned char>(cont)));
    } while (cont != 'N');

    std::cout << "Active sessions: ";
    traverseQueue(sessions);

    return 0;
}
