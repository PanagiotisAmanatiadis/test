/**
 * @file ex04_armstrong_numbers.cpp
 * @brief Prints all Armstrong numbers in the range [1, 999].
 *
 * An Armstrong number, as defined in this exercise, is a number equal to
 * the sum of the cubes of its own digits (narcissistic number for 3 digits).
 */

#include <iostream>

/**
 * @brief Checks whether @p x is an Armstrong number (sum of digit cubes).
 * @param x Non-negative integer to test (must be ≤ 999).
 * @return true if @p x equals the sum of the cubes of its digits.
 */
[[nodiscard]] bool isArmstrong(unsigned int x) {
    unsigned int sum{};
    unsigned int n = x;
    while (n) {
        const unsigned int digit = n % 10;
        sum += digit * digit * digit;
        n /= 10;
    }
    return sum == x;
}

int main() {
    std::cout << "Armstrong numbers in [1, 999]:\n";
    for (unsigned int i = 1; i < 1000; ++i) {
        if (isArmstrong(i)) {
            std::cout << i << '\n';
        }
    }
    return 0;
}
