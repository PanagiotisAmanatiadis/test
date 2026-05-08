/**
 * @file bst_depth.cpp
 * @brief Binary Search Tree of characters — recursive depth calculation.
 *
 * Inserts the characters of "PROCEDURE" into a BST (duplicates ignored),
 * then computes and prints the tree depth using a recursive function.
 */

#include <algorithm>
#include <iostream>
#include <memory>

/** @brief Node in a pointer-based BST. */
struct BSTNode {
    char                     data{};
    std::unique_ptr<BSTNode> left;
    std::unique_ptr<BSTNode> right;
};

// ── BST operations ────────────────────────────────────────────────────────────

[[nodiscard]] bool bstEmpty(const BSTNode* root) { return root == nullptr; }

/** @brief Recursively insert @p item into the BST rooted at @p root. */
void bstInsert(std::unique_ptr<BSTNode>& root, char item) {
    if (bstEmpty(root.get())) {
        root = std::make_unique<BSTNode>();
        root->data = item;
    } else if (item < root->data) {
        bstInsert(root->left, item);
    } else if (item > root->data) {
        bstInsert(root->right, item);
    } else {
        std::cout << '\'' << item << "' already in BST.\n";
    }
}

// ── Feature ──────────────────────────────────────────────────────────────────

/**
 * @brief Recursively compute the depth (height) of the BST.
 * @return 0 for an empty tree, or max(leftDepth, rightDepth) + 1 otherwise.
 */
[[nodiscard]] int bstDepth(const BSTNode* root) {
    if (bstEmpty(root)) return 0;
    return std::max(bstDepth(root->left.get()),
                    bstDepth(root->right.get())) + 1;
}

// ── Entry point ───────────────────────────────────────────────────────────────

int main() {
    std::unique_ptr<BSTNode> root;

    for (char c : {'P', 'R', 'O', 'C', 'E', 'D', 'U', 'R', 'E'})
        bstInsert(root, c);

    std::cout << "BST depth: " << bstDepth(root.get()) << '\n';

    return 0;
}
