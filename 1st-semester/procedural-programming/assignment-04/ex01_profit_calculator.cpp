/**
 * @file ex01_profit_calculator.cpp
 * @brief Computes profit and final sale amount from a purchase price and
 *        a profit rate percentage.
 */

#include <iomanip>
#include <iostream>

/** @brief Holds the computed profit and sale amount. */
struct ProfitResult {
    double profit{};
    double saleAmount{};
};

/**
 * @brief Calculates profit and total sale amount.
 * @param purchaseAmount  Net purchase cost.
 * @param ratePercent     Profit rate as an integer percentage (e.g. 20 for 20%).
 * @return ProfitResult with profit and saleAmount fields.
 */
[[nodiscard]] ProfitResult calculateProfit(long purchaseAmount, int ratePercent) {
    const double profit = static_cast<double>(purchaseAmount) * ratePercent / 100.0;
    return {profit, static_cast<double>(purchaseAmount) + profit};
}

int main() {
    long purchaseAmount{};
    int rate{};

    std::cout << "Enter the net purchase price: ";
    std::cin >> purchaseAmount;
    std::cout << "Enter the profit rate (%): ";
    std::cin >> rate;

    const auto result = calculateProfit(purchaseAmount, rate);

    std::cout << std::fixed << std::setprecision(2)
              << "Profit:      " << result.profit      << '\n'
              << "Sale amount: " << result.saleAmount  << '\n';
    return 0;
}
