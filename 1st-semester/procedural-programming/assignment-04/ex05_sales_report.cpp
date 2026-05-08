/**
 * @file ex05_sales_report.cpp
 * @brief Computes sales statistics for 4 salesmen across 5 product lines.
 *
 * Reports total income per salesman, commission (10% of income), and total
 * units sold per product.
 */

#include <array>
#include <iomanip>
#include <iostream>

namespace {
    constexpr int NUM_SALESMEN = 4;
    constexpr int NUM_PRODUCTS = 5;
    constexpr double COMMISSION_RATE = 0.10;

    constexpr std::array<int, NUM_PRODUCTS> PRICES{25000, 15000, 32000, 21000, 9200};

    constexpr std::array<std::array<int, NUM_PRODUCTS>, NUM_SALESMEN> SALES{{
        {10, 4,  5, 6, 7},
        { 7, 0, 12, 1, 3},
        { 4, 9,  5, 0, 8},
        { 3, 2,  1, 5, 6}
    }};
} // namespace

int main() {
    std::array<int, NUM_SALESMEN> incomePerSalesman{};
    std::array<int, NUM_PRODUCTS> quantityPerProduct{};

    for (int i = 0; i < NUM_SALESMEN; ++i) {
        for (int j = 0; j < NUM_PRODUCTS; ++j) {
            quantityPerProduct[j] += SALES[i][j];
            incomePerSalesman[i]  += SALES[i][j] * PRICES[j];
        }
    }

    std::cout << std::fixed << std::setprecision(2);

    std::cout << "Total income per salesman:";
    for (const auto income : incomePerSalesman) {
        std::cout << "  " << income;
    }
    std::cout << '\n';

    std::cout << "Commission per salesman:  ";
    for (const auto income : incomePerSalesman) {
        std::cout << "  " << static_cast<double>(income) * COMMISSION_RATE;
    }
    std::cout << '\n';

    std::cout << "Units sold per product:   ";
    for (const auto qty : quantityPerProduct) {
        std::cout << "  " << qty;
    }
    std::cout << '\n';

    return 0;
}
