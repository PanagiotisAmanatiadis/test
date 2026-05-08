/**
 * @file bst_right_node_count.cpp
 * @brief BST of integers — counts nodes on the rightmost path.
 *
 * Reads integers from stdin (sentinel -1 to stop), inserts them into a BST,
 * then counts the number of nodes on the path from the root by always
 * following right children (rightmost path length).
 */

#include <iostream>
#include <memory>

/** @brief Node in a pointer-based BST. */
struct BSTNode {
    int                      data{};
    std::unique_ptr<BSTNode> left;
    std::unique_ptr<BSTNode> right;
};

// ── BST helpers ───────────────────────────────────────────────────────────────

[[nodiscard]] bool bstEmpty(const BSTNode* root) { return root == nullptr; }

void bstInsert(std::unique_ptr<BSTNode>& root, int item) {
    if (bstEmpty(root.get())) {
        root = std::make_unique<BSTNode>();
        root->data = item;
    } else if (item < root->data) {
        bstInsert(root->left, item);
    } else if (item > root->data) {
        bstInsert(root->right, item);
    } else {
        std::cout << item << " already in BST.\n";
    }
}

// ── Feature ──────────────────────────────────────────────────────────────────

/**
 * @brief Count nodes on the rightmost path (root → rightmost leaf).
 *
 * At each level the function follows only the right child, counting every
 * node it visits (including the root and the leaf).
 *
 * @return 0 for an empty tree, otherwise the count of nodes on the path.
 */
[[nodiscard]] int rightNodeCount(const BSTNode* root) {
    if (bstEmpty(root)) return 0;
    return rightNodeCount(root->right.get()) + 1;
}

// ── Entry point ───────────────────────────────────────────────────────────────

int main() {
    std::unique_ptr<BSTNode> root;

    std::cout << "Enter integers to insert (-1 to stop):\n";
    int n{};
    while (std::cin >> n && n != -1)
        bstInsert(root, n);

    std::cout << "RightNodeCount = " << rightNodeCount(root.get()) << '\n';
    return 0;
}
