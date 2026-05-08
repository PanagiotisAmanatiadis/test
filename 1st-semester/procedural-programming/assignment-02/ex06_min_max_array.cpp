/**
 * @file ex06_min_max_array.cpp
 * @brief Reads integers from stdin (terminated by -1) and reports the
 *        minimum and maximum values in the sequence.
 */

#include <algorithm>
#include <iostream>
#include <vector>

#include "../include/Logger.hpp"

/**
 * @brief Reads integers from stdin until the sentinel value -1 is entered.
 * @return Vector of integers entered, excluding the sentinel.
 */
[[nodiscard]] std::vector<int> readIntegers() {
    std::cout << "Enter integers one per line. Enter -1 to finish:\n";
    std::vector<int> data;
    int value{};
    while (std::cin >> value && value != -1) {
        data.push_back(value);
    }
    return data;
}

int main() {
    const auto data = readIntegers();
    if (data.empty()) {
        Logger::error("No values were entered.");
        return 1;
    }

    const auto [minIt, maxIt] = std::minmax_element(data.cbegin(), data.cend());
    std::cout << "The range of values is " << *minIt << '-' << *maxIt << '\n';
    return 0;
}
