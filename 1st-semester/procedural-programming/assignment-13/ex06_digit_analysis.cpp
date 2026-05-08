/**
 * @file ex06_digit_analysis.cpp
 * @brief Reads a non-negative integer and reports its digit count,
 *        average digit value, and largest digit.
 */

#include <iomanip>
#include <iostream>

/** @brief Holds the decomposed digit statistics of an integer. */
struct DigitStats {
    long count{};
    double average{};
    long maxDigit{};
};

/**
 * @brief Decomposes a non-negative integer into digit statistics.
 * @param x  The integer to analyse (must be > 0).
 * @return DigitStats with count, average, and maxDigit populated.
 */
[[nodiscard]] DigitStats analyseDigits(long x) {
    long   count{};
    long   sum{};
    long   maxDigit{};

    while (x != 0) {
        const long digit = x % 10;
        ++count;
        sum += digit;
        if (digit > maxDigit) maxDigit = digit;
        x /= 10;
    }

    const double avg = (count > 0) ? static_cast<double>(sum) / count : 0.0;
    return {count, avg, maxDigit};
}

int main() {
    long x{};
    std::cout << "Enter a non-negative integer: ";
    std::cin >> x;

    const auto stats = analyseDigits(x);

    std::cout << std::fixed << std::setprecision(3)
              << "Digits:  " << stats.count    << '\n'
              << "Average: " << stats.average  << '\n'
              << "Max:     " << stats.maxDigit << '\n';
    return 0;
}
