/**
 * @file ex03_harmonic_number.cpp
 * @brief Computes and prints the N-th harmonic number H_N = Σ(1/i, i=1..N).
 */

#include <iostream>

/**
 * @brief Computes the N-th harmonic number.
 * @param n  Upper limit of the harmonic series (must be ≥ 1).
 * @return H_n = 1 + 1/2 + 1/3 + ... + 1/n.
 */
[[nodiscard]] double harmonicNumber(unsigned long n) {
    double h{};
    for (unsigned long i = 1; i <= n; ++i) {
        h += 1.0 / static_cast<double>(i);
    }
    return h;
}

int main() {
    constexpr unsigned long N = 100;
    std::cout << "H_" << N << " = " << harmonicNumber(N) << '\n';
    return 0;
}
