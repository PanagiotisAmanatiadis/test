/**
 * @file bst_teacher.cpp
 * @brief BST of teacher records — iterative insert/delete/search + subject search.
 *
 * Reads teacher records from I14F5.TXT (format: "name, number, code\n").
 * Keys on teacher name.  BSTSearchBySubject traverses all nodes and prints
 * every teacher whose subject code matches.
 */

#include <fstream>
#include <iostream>
#include <limits>
#include <memory>
#include <sstream>
#include <string>

/** @brief Teacher record stored in each BST node. */
struct Teacher {
    std::string name;
    std::string number;
    int         code{0};
};

/** @brief Node in a pointer-based BST keyed by teacher name. */
struct BSTNode {
    Teacher  data;
    BSTNode* left{nullptr};
    BSTNode* right{nullptr};
};

// ── BST helpers ───────────────────────────────────────────────────────────────

[[nodiscard]] bool bstEmpty(const BSTNode* root) { return root == nullptr; }

/** @brief Iterative insert (key = name). */
void bstInsert(BSTNode*& root, const Teacher& item) {
    BSTNode* loc    = root;
    BSTNode* parent = nullptr;
    bool     found  = false;

    while (!found && loc != nullptr) {
        parent = loc;
        if      (item.name < loc->data.name) loc = loc->left;
        else if (item.name > loc->data.name) loc = loc->right;
        else                                 found = true;
    }

    if (found) { std::cout << item.name << " already in BST.\n"; return; }

    auto* node   = new BSTNode{item, nullptr, nullptr};
    if (parent == nullptr)
        root = node;
    else if (item.name < parent->data.name)
        parent->left  = node;
    else
        parent->right = node;
}

/** @brief Iterative search; returns pointer to found node or nullptr. */
[[nodiscard]] BSTNode* bstSearch(BSTNode* root, const std::string& name) {
    while (!bstEmpty(root)) {
        if      (name < root->data.name) root = root->left;
        else if (name > root->data.name) root = root->right;
        else return root;
    }
    return nullptr;
}

/** @brief Iterative search that also records the parent. */
BSTNode* bstSearch2(BSTNode* root, const std::string& name, BSTNode*& parent) {
    parent = nullptr;
    while (!bstEmpty(root)) {
        if      (name < root->data.name) { parent = root; root = root->left; }
        else if (name > root->data.name) { parent = root; root = root->right; }
        else return root;
    }
    return nullptr;
}

void bstDelete(BSTNode*& root, const std::string& name) {
    BSTNode* parent{};
    BSTNode* n = bstSearch2(root, name, parent);
    if (!n) { std::cout << name << " not in BST.\n"; return; }

    BSTNode* subtree;
    if (n->left != nullptr && n->right != nullptr) {
        // Two children — replace with in-order successor.
        BSTNode* nNext  = n->right;
        BSTNode* pNext  = n;
        while (nNext->left != nullptr) { pNext = nNext; nNext = nNext->left; }
        n->data = nNext->data;
        n       = nNext;
        parent  = pNext;
    }
    subtree = (n->left != nullptr) ? n->left : n->right;
    if (parent == nullptr)
        root = subtree;
    else if (parent->left == n)
        parent->left  = subtree;
    else
        parent->right = subtree;
    delete n;
}

void inorder(const BSTNode* root) {
    if (!bstEmpty(root)) {
        inorder(root->left);
        std::cout << root->data.name   << ", "
                  << root->data.number << ", "
                  << root->data.code   << '\n';
        inorder(root->right);
    }
}

void destroyBST(BSTNode*& root) {
    if (!bstEmpty(root)) {
        destroyBST(root->left);
        destroyBST(root->right);
        delete root;
        root = nullptr;
    }
}

// ── Feature ──────────────────────────────────────────────────────────────────

/** @brief In-order traversal printing every teacher with matching @p code. */
void bstSearchBySubject(const BSTNode* root, int code) {
    if (!bstEmpty(root)) {
        bstSearchBySubject(root->left, code);
        if (root->data.code == code)
            std::cout << root->data.name   << ", "
                      << root->data.number << ", "
                      << root->data.code   << '\n';
        bstSearchBySubject(root->right, code);
    }
}

// ── File loader ───────────────────────────────────────────────────────────────

void buildBST(BSTNode*& root) {
    destroyBST(root);
    std::ifstream file("I14F5.TXT");
    if (!file) { std::cout << "Cannot open I14F5.TXT\n"; return; }

    std::string line;
    while (std::getline(file, line)) {
        std::istringstream ss(line);
        Teacher t;
        // Format: name, number, code
        if (!std::getline(ss, t.name,   ',')) continue;
        if (!std::getline(ss, t.number, ',')) continue;
        ss >> t.code;
        // Trim leading spaces.
        auto trim = [](std::string& s) {
            auto it = s.find_first_not_of(' ');
            if (it != std::string::npos) s = s.substr(it);
        };
        trim(t.name);
        trim(t.number);
        bstInsert(root, t);
    }
}

// ── Menu ─────────────────────────────────────────────────────────────────────

int readChoice() {
    int c{};
    std::cout << "\n--- MENU ---\n"
              << "1. Build BST from file\n"
              << "2. Insert teacher\n"
              << "3. Delete teacher\n"
              << "4. Search by name\n"
              << "5. Search by subject code\n"
              << "6. Print all (in-order)\n"
              << "7. Quit\n"
              << "Choice: ";
    while (!(std::cin >> c) || c < 1 || c > 7) {
        std::cin.clear();
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
        std::cout << "Choice (1-7): ";
    }
    return c;
}

int main() {
    BSTNode* root{nullptr};

    int choice{};
    do {
        choice = readChoice();
        switch (choice) {
        case 1:
            buildBST(root);
            std::cout << "BST built.\n";
            break;

        case 2: {
            Teacher t;
            std::cin.ignore();
            std::cout << "Name: ";    std::getline(std::cin, t.name);
            std::cout << "Number: ";  std::getline(std::cin, t.number);
            std::cout << "Code: ";    std::cin >> t.code;
            bstInsert(root, t);
            break;
        }

        case 3:
            if (bstEmpty(root)) { std::cout << "Empty tree.\n"; break; }
            {
                std::cin.ignore();
                std::string name;
                std::cout << "Name to delete: ";
                std::getline(std::cin, name);
                bstDelete(root, name);
            }
            break;

        case 4:
            if (bstEmpty(root)) { std::cout << "Empty tree.\n"; break; }
            {
                std::cin.ignore();
                std::string name;
                std::cout << "Name to search: ";
                std::getline(std::cin, name);
                BSTNode* found = bstSearch(root, name);
                if (found)
                    std::cout << found->data.name   << ", "
                              << found->data.number << ", "
                              << found->data.code   << '\n';
                else
                    std::cout << name << " not found.\n";
            }
            break;

        case 5: {
            int code{};
            std::cout << "Subject code: ";
            std::cin >> code;
            bstSearchBySubject(root, code);
            break;
        }

        case 6:
            if (bstEmpty(root)) std::cout << "Empty tree.\n";
            else inorder(root);
            break;

        case 7:
            break;
        }
    } while (choice != 7);

    destroyBST(root);
    return 0;
}
