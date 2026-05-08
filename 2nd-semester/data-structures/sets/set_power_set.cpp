/**
 * @file set_power_set.cpp
 * @brief Boolean-array set ADT — generates and prints the power set.
 *
 * The universe has 6 elements (indices 1–5).  The power set contains 2^6 = 64
 * subsets, numbered 0–63.  Each subset is represented by a boolean array of
 * size 6.  A bitmask approach fills each subset: bit j set in mask i means
 * element j belongs to subset i.  Only the odd-indexed subsets are printed.
 */

#include <array>
#include <cmath>
#include <iostream>
#include <vector>

namespace {
    constexpr int SET_SIZE   = 6;
    constexpr int POWER_SIZE = 1 << SET_SIZE;   // 2^6 = 64
}

/** @brief Boolean-array set over indices [0, SET_SIZE). */
using Set = std::array<bool, SET_SIZE>;

void create(Set& s)           { s.fill(false); }
void insert(int elem, Set& s) { s[elem] = true; }
[[nodiscard]] bool member(int elem, const Set& s) { return s[elem]; }

// ── Feature ──────────────────────────────────────────────────────────────────

/**
 * @brief Fill @p powerSet so that subset i contains element j iff bit j is
 *        set in the binary representation of i.
 */
void createPowerSet(std::vector<Set>& powerSet) {
    for (int i = 1; i < POWER_SIZE; ++i)
        for (int j = 1; j < SET_SIZE; ++j)
            if (i & (1 << j))
                insert(j, powerSet[i]);
}

// ── Entry point ──────────────────────────────────────────────────────────────

int main() {
    std::vector<Set> powerSet(POWER_SIZE);
    for (auto& s : powerSet) create(s);

    createPowerSet(powerSet);

    // Print odd-indexed subsets (matches original exercise output).
    for (int i = 1; i < POWER_SIZE; i += 2) {
        for (int j = 1; j < SET_SIZE; ++j)
            if (member(j, powerSet[i]))
                std::cout << j << ' ';
        std::cout << '\n';
    }

    return 0;
}
