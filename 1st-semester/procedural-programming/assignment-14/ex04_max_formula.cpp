/**
 * @file ex04_max_formula.cpp
 * @brief Reads three integers a, b, c and computes
 *        Y = (2 × max(a, b) + 3 × greatest(a, b, c)) / 4.
 */

#include <algorithm>
#include <iostream>

/**
 * @brief Returns the greatest of three integers.
 * @param a First value.
 * @param b Second value.
 * @param c Third value.
 * @return Maximum of a, b, c.
 */
[[nodiscard]] int greatest(int a, int b, int c) {
    return std::max({a, b, c});
}

/**
 * @brief Computes Y from three integer inputs.
 * @param a First value.
 * @param b Second value.
 * @param c Third value.
 * @return (2 × max(a,b) + 3 × greatest(a,b,c)) / 4.
 */
[[nodiscard]] int computeY(int a, int b, int c) {
    return (2 * std::max(a, b) + 3 * greatest(a, b, c)) / 4;
}

int main() {
    int a{}, b{}, c{};
    std::cout << "Enter a: "; std::cin >> a;
    std::cout << "Enter b: "; std::cin >> b;
    std::cout << "Enter c: "; std::cin >> c;

    std::cout << "Y = " << computeY(a, b, c) << '\n';
    return 0;
}
