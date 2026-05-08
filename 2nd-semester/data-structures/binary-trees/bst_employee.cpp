/**
 * @file bst_employee.cpp
 * @brief Three BSTs of employee records partitioned by department code.
 *
 * Reads employee records (surname, name, department code) from a file
 * (I13F5.txt), inserts each into the appropriate BST:
 *   - code 1 → office staff
 *   - code 2 → workers
 *   - code 3 → representatives
 *
 * Supports insert, search (by surname + code), and in-order traversal via menu.
 */

#include <fstream>
#include <iostream>
#include <limits>
#include <memory>
#include <string>

/** @brief Employee record stored in each BST node. */
struct Employee {
    std::string surname;
    std::string name;
    int         code{0};
};

/** @brief Node in a pointer-based BST keyed by surname. */
struct BSTNode {
    Employee                 data;
    std::unique_ptr<BSTNode> left;
    std::unique_ptr<BSTNode> right;
};

// ── BST operations ────────────────────────────────────────────────────────────

[[nodiscard]] bool bstEmpty(const BSTNode* root) { return root == nullptr; }

void bstInsert(std::unique_ptr<BSTNode>& root, const Employee& item) {
    if (bstEmpty(root.get())) {
        root = std::make_unique<BSTNode>();
        root->data = item;
    } else if (item.surname < root->data.surname) {
        bstInsert(root->left, item);
    } else if (item.surname > root->data.surname) {
        bstInsert(root->right, item);
    } else {
        std::cout << item.surname << " already in BST.\n";
    }
}

/** @brief Search by surname; returns pointer to found node or nullptr. */
[[nodiscard]] const BSTNode* bstSearch(const BSTNode* root,
                                        const std::string& surname)
{
    if (bstEmpty(root)) return nullptr;
    if (surname < root->data.surname) return bstSearch(root->left.get(),  surname);
    if (surname > root->data.surname) return bstSearch(root->right.get(), surname);
    return root;
}

void bstInorder(const BSTNode* root) {
    if (!bstEmpty(root)) {
        bstInorder(root->left.get());
        std::cout << '(' << root->data.surname << ", "
                  << root->data.name          << ", "
                  << root->data.code          << "), ";
        bstInorder(root->right.get());
    }
}

// ── File loader ───────────────────────────────────────────────────────────────

void buildBSTs(std::unique_ptr<BSTNode>& root1,
               std::unique_ptr<BSTNode>& root2,
               std::unique_ptr<BSTNode>& root3)
{
    root1.reset();
    root2.reset();
    root3.reset();

    std::ifstream file("I13F5.txt");
    if (!file) { std::cout << "Cannot open I13F5.txt\n"; return; }

    Employee emp;
    while (file >> emp.surname >> emp.name >> emp.code) {
        if      (emp.code == 1) bstInsert(root1, emp);
        else if (emp.code == 2) bstInsert(root2, emp);
        else                    bstInsert(root3, emp);
    }
}

// ── Menu helpers ──────────────────────────────────────────────────────────────

int readChoice() {
    int c{};
    std::cout << "\n--- MENU ---\n"
              << "1. Build BSTs from file\n"
              << "2. Insert employee\n"
              << "3. Search employee\n"
              << "4. Traverse in-order (all departments)\n"
              << "5. Quit\n"
              << "Choice: ";
    while (!(std::cin >> c) || c < 1 || c > 5) {
        std::cin.clear();
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
        std::cout << "Choice (1-5): ";
    }
    return c;
}

const std::unique_ptr<BSTNode>& selectTree(int code,
    std::unique_ptr<BSTNode>& r1,
    std::unique_ptr<BSTNode>& r2,
    std::unique_ptr<BSTNode>& r3)
{
    if (code == 1) return r1;
    if (code == 2) return r2;
    return r3;
}

// ── Entry point ───────────────────────────────────────────────────────────────

int main() {
    std::unique_ptr<BSTNode> root1, root2, root3;

    int choice{};
    do {
        choice = readChoice();
        switch (choice) {
        case 1:
            buildBSTs(root1, root2, root3);
            std::cout << "BSTs built from file.\n";
            break;

        case 2: {
            Employee emp;
            std::cout << "Surname: ";
            std::cin >> emp.surname;
            std::cout << "Name: ";
            std::cin >> emp.name;
            std::cout << "Code (1=office,2=worker,3=representative): ";
            std::cin >> emp.code;
            auto& tree = selectTree(emp.code, root1, root2, root3);
            bstInsert(const_cast<std::unique_ptr<BSTNode>&>(tree), emp);
            break;
        }

        case 3: {
            std::string surname;
            int code{};
            std::cout << "Surname: ";
            std::cin >> surname;
            std::cout << "Code (1/2/3): ";
            std::cin >> code;
            const auto& tree = selectTree(code, root1, root2, root3);
            if (bstEmpty(tree.get())) {
                std::cout << "Empty tree.\n";
            } else {
                const BSTNode* found = bstSearch(tree.get(), surname);
                if (found)
                    std::cout << found->data.surname << ' '
                              << found->data.name    << ' '
                              << found->data.code    << '\n';
                else
                    std::cout << "Employee not found.\n";
            }
            break;
        }

        case 4:
            std::cout << "Office staff:\n";
            bstEmpty(root1.get()) ? std::cout << "  (empty)\n"
                                  : (bstInorder(root1.get()), std::cout << '\n');
            std::cout << "Workers:\n";
            bstEmpty(root2.get()) ? std::cout << "  (empty)\n"
                                  : (bstInorder(root2.get()), std::cout << '\n');
            std::cout << "Representatives:\n";
            bstEmpty(root3.get()) ? std::cout << "  (empty)\n"
                                  : (bstInorder(root3.get()), std::cout << '\n');
            break;

        case 5:
            break;
        }
    } while (choice != 5);

    return 0;
}
