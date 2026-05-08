/**
 * @file ex03_multiplication_table.cpp
 * @brief Prints a 10×10 multiplication table with row headers.
 */

#include <iomanip>
#include <iostream>

int main() {
    for (int i = 1; i <= 10; ++i) {
        std::cout << std::setw(4) << i;
        for (int j = 1; j <= 10; ++j) {
            std::cout << std::setw(4) << i * j;
        }
        std::cout << '\n';
    }
    return 0;
}
