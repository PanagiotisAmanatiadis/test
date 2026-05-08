/**
 * @file ex04_series_sum.cpp
 * @brief Computes and prints the arithmetic series sum 1 + 2 + ... + N
 *        using the closed-form formula N×(N+1)/2.
 */

#include <iostream>

/**
 * @brief Computes the sum of the arithmetic series 1 + 2 + ... + n.
 * @param n  Upper limit (must be ≥ 0).
 * @return n × (n + 1) / 2.
 */
[[nodiscard]] constexpr unsigned long seriesSum(unsigned long n) noexcept {
    return (1UL + n) * n / 2UL;
}

int main() {
    std::cout << "Sum 1.." << 100  << " = " << seriesSum(100)  << '\n';
    std::cout << "Sum 1.." << 1000 << " = " << seriesSum(1000) << '\n';
    return 0;
}
