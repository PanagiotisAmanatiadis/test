/**
 * @file ex05_array_occurrences.cpp
 * @brief Populates a 50-element array with random single digits [0,9],
 *        then reports how many times a user-specified digit appears and
 *        at which positions.
 */

#include <cstdlib>
#include <ctime>
#include <iostream>
#include <vector>

int main() {
    std::srand(static_cast<unsigned>(std::time(nullptr)));

    constexpr int COUNT = 50;
    std::vector<int> data(COUNT);

    for (auto& v : data) {
        v = std::rand() / (RAND_MAX / 10 + 1);
    }

    std::cout << "Array contents:\n";
    for (const auto v : data) {
        std::cout << v << ' ';
    }
    std::cout << "\n--------------\n";

    int target{};
    std::cout << "Enter a digit (0–9): ";
    std::cin >> target;

    std::vector<int> positions;
    for (int i = 0; i < COUNT; ++i) {
        if (data[i] == target) {
            positions.push_back(i);
        }
    }

    const int times = static_cast<int>(positions.size());
    std::cout << "The digit " << target << " appears " << times
              << (times != 1 ? " times" : " time") << ".\n"
              << "Positions:\n";
    for (const auto pos : positions) {
        std::cout << ' ' << pos;
    }
    std::cout << "\n-----------------\n";
    return 0;
}
