/**
 * @file bst_random_generate.cpp
 * @brief BST of characters — iterative insert, random generation.
 *
 * Reads N from stdin, generates N random uppercase letters (A–Z), inserts
 * each into a BST using an iterative algorithm, then prints the result
 * in ascending order via in-order traversal.  Duplicate letters are silently
 * skipped (BST property — each key appears at most once).
 */

#include <algorithm>
#include <cstdlib>
#include <ctime>
#include <iostream>
#include <memory>

/** @brief Node in a pointer-based BST. */
struct BSTNode {
    char     data{};
    BSTNode* left{nullptr};
    BSTNode* right{nullptr};
};

// ── BST helpers ───────────────────────────────────────────────────────────────

[[nodiscard]] bool bstEmpty(const BSTNode* root) { return root == nullptr; }

/**
 * @brief Iterative BST insert.
 * @param root  Root pointer (updated when inserting into an empty tree).
 * @param item  Character to insert.
 */
void bstInsert(BSTNode*& root, char item) {
    BSTNode* loc    = root;
    BSTNode* parent = nullptr;
    bool     found  = false;

    while (!found && loc != nullptr) {
        parent = loc;
        if      (item < loc->data) loc = loc->left;
        else if (item > loc->data) loc = loc->right;
        else                       found = true;
    }

    if (found) return;   // duplicate — skip silently

    auto* node   = new BSTNode{item, nullptr, nullptr};
    if (parent == nullptr)
        root = node;
    else if (item < parent->data)
        parent->left  = node;
    else
        parent->right = node;
}

void inorder(const BSTNode* root) {
    if (!bstEmpty(root)) {
        inorder(root->left);
        std::cout << root->data << ' ';
        inorder(root->right);
    }
}

/** @brief Free all nodes (post-order). */
void destroyBST(BSTNode*& root) {
    if (!bstEmpty(root)) {
        destroyBST(root->left);
        destroyBST(root->right);
        delete root;
        root = nullptr;
    }
}

// ── Feature ──────────────────────────────────────────────────────────────────

/**
 * @brief Generate @p n random uppercase letters and insert each into @p root.
 */
void generateBST(BSTNode*& root, int n) {
    for (int i = 0; i < n; ++i) {
        char ch = static_cast<char>('A' + std::rand() % 26);
        bstInsert(root, ch);
    }
}

// ── Entry point ───────────────────────────────────────────────────────────────

int main() {
    std::srand(static_cast<unsigned>(std::time(nullptr)));

    int n{};
    std::cout << "Number of letters: ";
    std::cin >> n;

    BSTNode* tree{nullptr};
    generateBST(tree, n);

    std::cout << "In-order: ";
    inorder(tree);
    std::cout << '\n';

    destroyBST(tree);
    return 0;
}
