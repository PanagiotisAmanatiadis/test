/**
 * @file hash_table_chaining.cpp
 * @brief Hash table with chaining (synonym lists) for user records.
 *
 * Implements a static hash table (HMax=10 buckets, VMax=30 slots) using
 * a flat array (List) whose free slots are chained as a stack.  Collisions
 * are resolved by chaining synonyms within the same array.
 *
 * Each record stores: integer key, user name, and a role code
 * (1=student, 2=postgraduate, 3=teacher, 4=visitor).
 */

#include <array>
#include <iostream>
#include <limits>
#include <string>

namespace {
    constexpr int H_MAX       = 10;
    constexpr int V_MAX       = 30;
    constexpr int END_OF_LIST = -1;
}

constexpr std::array<const char*, 4> ROLES{"student", "postgraduate student",
                                            "teacher", "visitor"};

/** @brief User payload stored in each hash-list node. */
struct UserData {
    std::string name;
    int         code{0};
};

/** @brief One slot in the flat storage array. */
struct ListElm {
    int      recKey{0};
    UserData data;
    int      link{END_OF_LIST};
};

/** @brief Hash table with chaining built over a flat array. */
struct HashList {
    std::array<int, H_MAX>      hashTable{};
    std::array<ListElm, V_MAX>  list{};
    int size{0};
    int stackPtr{0};
    int subListPtr{END_OF_LIST};
};

// ── Primitives ────────────────────────────────────────────────────────────────

[[nodiscard]] int hashKey(int key) { return key % H_MAX; }

[[nodiscard]] bool isFull(const HashList& h) { return h.size == V_MAX; }

void create(HashList& h) {
    h.size     = 0;
    h.stackPtr = 0;
    h.hashTable.fill(END_OF_LIST);
    for (int i = 0; i < V_MAX - 1; ++i) {
        h.list[i].link        = i + 1;
        h.list[i].data.name   = "";
        h.list[i].data.code   = 0;
    }
    h.list[V_MAX - 1].link = END_OF_LIST;
}

// ── Search ────────────────────────────────────────────────────────────────────

/** @brief Search within the synonym sublist starting at @p h.subListPtr. */
void searchSynonymList(const HashList& h, int keyArg, int& loc, int& pred) {
    int next = h.subListPtr;
    loc  = END_OF_LIST;
    pred = END_OF_LIST;
    while (next != END_OF_LIST) {
        if (h.list[next].recKey == keyArg) {
            loc  = next;
            return;
        }
        pred = next;
        next = h.list[next].link;
    }
}

/** @brief Search the full hash table for @p keyArg. */
void searchHashList(HashList& h, int keyArg, int& loc, int& pred) {
    int hVal = hashKey(keyArg);
    if (h.hashTable[hVal] == END_OF_LIST) {
        loc = pred = END_OF_LIST;
        return;
    }
    h.subListPtr = h.hashTable[hVal];
    searchSynonymList(h, keyArg, loc, pred);
}

// ── Mutation ──────────────────────────────────────────────────────────────────

void addRecord(HashList& h, const ListElm& rec) {
    if (isFull(h)) {
        std::cout << "Full hash list.\n";
        return;
    }
    int loc{}, pred{};
    // We need non-const search — use a local copy of subListPtr.
    {
        int hVal = hashKey(rec.recKey);
        if (h.hashTable[hVal] == END_OF_LIST) {
            loc = pred = END_OF_LIST;
        } else {
            h.subListPtr = h.hashTable[hVal];
            searchSynonymList(h, rec.recKey, loc, pred);
        }
    }
    if (loc != END_OF_LIST) {
        std::cout << "Duplicate key " << rec.recKey << " — not inserted.\n";
        return;
    }
    int newSlot    = h.stackPtr;
    h.stackPtr     = h.list[newSlot].link;
    h.list[newSlot] = rec;
    ++h.size;

    int hVal = hashKey(rec.recKey);
    if (pred == END_OF_LIST) {
        h.list[newSlot].link = h.hashTable[hVal];
        h.hashTable[hVal]    = newSlot;
    } else {
        h.list[newSlot].link = h.list[pred].link;
        h.list[pred].link    = newSlot;
    }
}

void deleteRecord(HashList& h, int delKey) {
    int loc{}, pred{};
    searchHashList(h, delKey, loc, pred);
    if (loc == END_OF_LIST) {
        std::cout << "No record with key " << delKey << ".\n";
        return;
    }
    if (pred != END_OF_LIST) {
        h.list[pred].link = h.list[loc].link;
    } else {
        int hVal = hashKey(delKey);
        h.hashTable[hVal] = h.list[loc].link;
    }
    h.list[loc].link = h.stackPtr;
    h.stackPtr       = loc;
    --h.size;
}

// ── Display ───────────────────────────────────────────────────────────────────

void printHashList(const HashList& h) {
    std::cout << "Synonym chains:\n";
    for (int i = 0; i < H_MAX; ++i) {
        int idx = h.hashTable[i];
        if (idx != END_OF_LIST)
            std::cout << "Bucket " << i << " (collision key mod " << H_MAX << "):\n";
        while (idx != END_OF_LIST) {
            const auto& rec = h.list[idx];
            const char* role = (rec.data.code >= 1 && rec.data.code <= 4)
                               ? ROLES[static_cast<std::size_t>(rec.data.code - 1)]
                               : "unknown";
            std::cout << "  [" << rec.recKey << ", " << rec.data.name
                      << ", " << role << "]\n";
            idx = rec.link;
        }
    }
}

// ── Menu ─────────────────────────────────────────────────────────────────────

int readChoice() {
    int c{};
    std::cout << "\n--- MENU ---\n"
              << "1. Create hash list\n"
              << "2. Insert record\n"
              << "3. Delete record\n"
              << "4. Search record\n"
              << "5. Print all records\n"
              << "6. Quit\n"
              << "Choice: ";
    while (!(std::cin >> c) || c < 1 || c > 6) {
        std::cin.clear();
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
        std::cout << "Choice (1-6): ";
    }
    return c;
}

int main() {
    HashList h;
    create(h);

    int choice{};
    do {
        choice = readChoice();
        switch (choice) {
        case 1:
            create(h);
            std::cout << "Hash list created.\n";
            break;

        case 2: {
            char cont{'Y'};
            do {
                ListElm rec;
                rec.link = END_OF_LIST;
                std::cout << "Key: ";
                std::cin >> rec.recKey;
                std::cin.ignore();
                std::cout << "Name: ";
                std::getline(std::cin, rec.data.name);
                std::cout << "Code (1=student,2=postgrad,3=teacher,4=visitor): ";
                std::cin >> rec.data.code;
                addRecord(h, rec);
                std::cout << "Continue? (Y/N): ";
                std::cin >> cont;
            } while (std::toupper(static_cast<unsigned char>(cont)) != 'N');
            break;
        }

        case 3: {
            char cont{'Y'};
            do {
                int key{};
                std::cout << "Key to delete: ";
                std::cin >> key;
                deleteRecord(h, key);
                std::cout << "Continue? (Y/N): ";
                std::cin >> cont;
            } while (std::toupper(static_cast<unsigned char>(cont)) != 'N');
            break;
        }

        case 4: {
            char cont{'Y'};
            do {
                int key{};
                std::cout << "Key to search: ";
                std::cin >> key;
                int loc{}, pred{};
                searchHashList(h, key, loc, pred);
                if (loc != END_OF_LIST) {
                    const auto& rec = h.list[loc];
                    const char* role = (rec.data.code >= 1 && rec.data.code <= 4)
                                       ? ROLES[static_cast<std::size_t>(rec.data.code - 1)]
                                       : "unknown";
                    std::cout << "Found: [" << rec.recKey << ", " << rec.data.name
                              << ", " << role << "]\n";
                } else {
                    std::cout << "No record with key " << key << ".\n";
                }
                std::cout << "Continue? (Y/N): ";
                std::cin >> cont;
            } while (std::toupper(static_cast<unsigned char>(cont)) != 'N');
            break;
        }

        case 5:
            printHashList(h);
            break;

        case 6:
            break;
        }
    } while (choice != 6);

    return 0;
}
