/**
 * @file ex07_digit_sum.cpp
 * @brief Reads an alphanumeric string and prints all digit characters with
 *        '+' between them, followed by their total sum.
 *
 * Example: "ab3c5" → "3 + 5 = 8"
 */

#include <cctype>
#include <iostream>
#include <string>

/**
 * @brief Prints the digit-sum expression for the given string.
 * @param s  Input string (may contain letters, digits, or other characters).
 */
void printDigitSum(const std::string& s) {
    unsigned int sum{};
    bool first = true;

    for (const char ch : s) {
        if (std::isdigit(static_cast<unsigned char>(ch))) {
            if (!first) std::cout << " + ";
            std::cout << ch;
            sum += static_cast<unsigned int>(ch - '0');
            first = false;
        }
    }
    std::cout << " = " << sum << '\n';
}

int main() {
    std::cout << "Enter an alphanumeric string: ";
    std::string s;
    std::getline(std::cin, s);

    printDigitSum(s);
    return 0;
}
