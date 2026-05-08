/**
 * @file ex05_array_rotation.cpp
 * @brief Reads 5 integers into an array, moves the last element to the
 *        front (right-rotation by one), and prints the result.
 */

#include <algorithm>
#include <array>
#include <iostream>

int main() {
    constexpr int SIZE = 5;
    std::array<int, SIZE> data{};

    std::cout << "Enter " << SIZE << " integers:\n";
    for (auto& v : data) {
        std::cout << "Value: ";
        std::cin >> v;
    }

    // Rotate right by one: last element moves to front
    std::rotate(data.rbegin(), data.rbegin() + 1, data.rend());

    std::cout << "Rotated array:";
    for (const auto v : data) {
        std::cout << ' ' << v;
    }
    std::cout << '\n';
    return 0;
}
