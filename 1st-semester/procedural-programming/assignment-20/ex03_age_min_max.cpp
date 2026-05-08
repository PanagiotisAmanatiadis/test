/**
 * @file ex03_age_min_max.cpp
 * @brief Reads ages from stdin until -1 is entered, then reports the
 *        minimum and maximum age seen.
 */

#include <iostream>
#include <limits>

int main() {
    std::cout << "Enter ages one per line. Enter -1 to stop.\n";

    int x{};
    std::cout << "Age: ";
    std::cin >> x;

    if (x == -1) {
        std::cout << "No ages were entered.\n";
        return 0;
    }

    int minAge = x;
    int maxAge = x;

    while (std::cout << "Age: ", std::cin >> x, x != -1) {
        if (x > maxAge) maxAge = x;
        if (x < minAge) minAge = x;
    }

    std::cout << "Maximum age: " << maxAge << '\n'
              << "Minimum age: " << minAge << '\n';
    return 0;
}
