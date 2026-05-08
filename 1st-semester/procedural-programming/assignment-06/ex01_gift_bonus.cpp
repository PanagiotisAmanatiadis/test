/**
 * @file ex01_gift_bonus.cpp
 * @brief Calculates an annual gift/bonus from days worked, daily wage,
 *        and a bonus rate.
 */

#include <iomanip>
#include <iostream>

/**
 * @brief Computes the annual bonus amount.
 * @param days  Number of working days in the year.
 * @param wage  Daily wage.
 * @param rate  Bonus rate as a fraction (e.g. 0.25 for 25%).
 * @return Bonus amount.
 */
[[nodiscard]] double calculateBonus(int days, long wage, double rate) {
    return static_cast<double>(days) * static_cast<double>(wage) * rate;
}

int main() {
    int days{};
    long wage{};
    double rate{};

    std::cout << "Enter working days in the year: ";
    std::cin >> days;
    std::cout << "Enter daily wage: ";
    std::cin >> wage;
    std::cout << "Enter bonus rate (e.g. 0.25): ";
    std::cin >> rate;

    std::cout << std::fixed << std::setprecision(2)
              << "Annual bonus: " << calculateBonus(days, wage, rate) << '\n';
    return 0;
}
