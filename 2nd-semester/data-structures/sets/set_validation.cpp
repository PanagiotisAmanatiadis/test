/**
 * @file set_validation.cpp
 * @brief Boolean-array set ADT — validates integers and identifiers.
 *
 * Implements a set over ASCII character codes (size 255) using a boolean array.
 * Builds three sets (CharacterSet for sign characters, DigitSet, LetterSet),
 * then validates user-entered strings as integers or identifiers using set
 * membership tests.
 *
 * A valid integer starts with an optional '+'/'-' followed only by digits.
 * A valid identifier starts with a letter or '_' followed by letters, digits, or '_'.
 */

#include <array>
#include <cctype>
#include <iostream>
#include <string>

namespace {
    constexpr int SET_SIZE = 255;
}

/** @brief Boolean-array set over indices [0, SET_SIZE). */
using Set = std::array<bool, SET_SIZE>;

// ── Set primitives ────────────────────────────────────────────────────────────

void create(Set& s)              { s.fill(false); }
void insert(int elem, Set& s)    { s[elem] = true; }
void remove(int elem, Set& s)    { s[elem] = false; }
[[nodiscard]] bool member(int elem, const Set& s) { return s[elem]; }

// ── Validation ────────────────────────────────────────────────────────────────

/**
 * @brief Returns true if @p str represents a valid integer.
 *
 * Grammar: ['+' | '-'] digit+
 */
[[nodiscard]] bool isValidInteger(const Set& charSet, const Set& digitSet,
                                   const std::string& str)
{
    if (str.empty()) return false;
    std::size_t pos = 0;
    if (member(static_cast<unsigned char>(str[0]), charSet))
        ++pos;                              // optional sign character
    if (pos >= str.size()) return false;   // nothing after sign
    for (; pos < str.size(); ++pos)
        if (!member(static_cast<unsigned char>(str[pos]), digitSet))
            return false;
    return true;
}

/**
 * @brief Returns true if @p str is a valid identifier.
 *
 * Grammar: (letter | '_') (letter | digit | '_')*
 */
[[nodiscard]] bool isValidIdentifier(const Set& letterSet, const Set& digitSet,
                                      const std::string& str)
{
    if (str.empty()) return false;
    if (!member(static_cast<unsigned char>(str[0]), letterSet))
        return false;
    for (std::size_t i = 1; i < str.size(); ++i) {
        unsigned char c = static_cast<unsigned char>(str[i]);
        if (!member(c, letterSet) && !member(c, digitSet))
            return false;
    }
    return true;
}

// ── Entry point ───────────────────────────────────────────────────────────────

int main() {
    Set charSet, digitSet, letterSet;
    create(charSet);
    create(digitSet);
    create(letterSet);

    // '+' (43) and '-' (45)
    insert(43, charSet);
    insert(45, charSet);

    // Digits '0'–'9' (48–57)
    for (int i = 48; i <= 57; ++i) insert(i, digitSet);

    // Letters 'A'–'Z' (65–90), 'a'–'z' (97–122), '_' (95)
    for (int i = 65; i <= 90; ++i)  insert(i, letterSet);
    for (int i = 97; i <= 122; ++i) insert(i, letterSet);
    insert(95, letterSet);

    // --- Integer validation loop ---
    char cont{'Y'};
    do {
        std::string input;
        std::cout << "Enter an integer: ";
        std::cin >> input;
        std::cout << (isValidInteger(charSet, digitSet, input)
                      ? "Valid integer" : "Not a valid integer") << '\n';
        std::cout << "Continue? (Y/N): ";
        std::cin >> cont;
    } while (std::toupper(static_cast<unsigned char>(cont)) != 'N');

    // --- Identifier validation loop ---
    cont = 'Y';
    do {
        std::string input;
        std::cout << "Enter an identifier: ";
        std::cin >> input;
        std::cout << (isValidIdentifier(letterSet, digitSet, input)
                      ? "Valid identifier" : "Not a valid identifier") << '\n';
        std::cout << "Continue? (Y/N): ";
        std::cin >> cont;
    } while (std::toupper(static_cast<unsigned char>(cont)) != 'N');

    return 0;
}
