/**
 * @file huffman_decoder.cpp
 * @brief Huffman decoding tree — builds from code table and decodes a message.
 *
 * Reads a Huffman code table from `codesRW.txt` (format: "symbol code\n"),
 * builds a decoding binary tree (0 = go left, 1 = go right), then decodes
 * the bit stream in `program.txt`, printing each decoded symbol.
 */

#include <fstream>
#include <iostream>
#include <memory>
#include <string>

/** @brief Node in the Huffman decoding tree. */
struct TreeNode {
    std::string              symbol;        ///< leaf: decoded symbol; internal: empty
    std::unique_ptr<TreeNode> left;
    std::unique_ptr<TreeNode> right;

    [[nodiscard]] bool isLeaf() const {
        return left == nullptr && right == nullptr;
    }
};

// ── Tree construction ─────────────────────────────────────────────────────────

/**
 * @brief Insert a symbol into the decoding tree following @p code.
 * @param root     Root of the Huffman tree.
 * @param symbol   The symbol to store at the leaf.
 * @param code     Binary string of '0'/'1' characters representing the path.
 */
void addToTree(TreeNode& root, const std::string& symbol,
               const std::string& code)
{
    TreeNode* p = &root;
    for (char bit : code) {
        if (bit == '0') {
            if (!p->left)  p->left  = std::make_unique<TreeNode>();
            p = p->left.get();
        } else {
            if (!p->right) p->right = std::make_unique<TreeNode>();
            p = p->right.get();
        }
    }
    p->symbol = symbol;
}

/**
 * @brief Build the Huffman decoding tree from @p codeFile.
 * @param codeFile  Open input stream; each line: "symbol code"
 * @return Unique pointer to the root of the constructed tree.
 */
[[nodiscard]] std::unique_ptr<TreeNode> buildDecodingTree(std::istream& codeFile)
{
    auto root = std::make_unique<TreeNode>();
    std::string symbol, code;
    while (codeFile >> symbol >> code)
        addToTree(*root, symbol, code);
    return root;
}

// ── Decoding ──────────────────────────────────────────────────────────────────

/**
 * @brief Decode the bit stream in @p messageFile using the Huffman tree.
 *
 * Traverses the tree following each '0'/'1' bit; when a leaf is reached the
 * stored symbol is printed and traversal restarts from the root.
 * Newlines and any non-bit characters in the file are passed through as-is.
 */
void decode(const TreeNode& root, std::istream& messageFile) {
    const TreeNode* p = &root;
    char bit{};
    while (messageFile.get(bit)) {
        if (bit == '0' || bit == '1') {
            std::cout << bit;                    // echo the bit
            p = (bit == '0') ? p->left.get() : p->right.get();
            if (p == nullptr) {
                std::cout << "\n[decode error: null path]\n";
                p = &root;
                continue;
            }
            if (p->isLeaf()) {
                std::cout << "---" << p->symbol << '\n';
                p = &root;
            }
        } else if (bit != '\n') {
            std::cout << "[unexpected bit: " << bit << "]\n";
        }
    }
}

// ── Entry point ───────────────────────────────────────────────────────────────

int main() {
    std::ifstream codeFile("codesRW.txt");
    if (!codeFile) { std::cerr << "Cannot open codesRW.txt\n"; return 1; }

    auto root = buildDecodingTree(codeFile);

    std::ifstream msgFile("program.txt");
    if (!msgFile) { std::cerr << "Cannot open program.txt\n"; return 1; }

    decode(*root, msgFile);
    return 0;
}
