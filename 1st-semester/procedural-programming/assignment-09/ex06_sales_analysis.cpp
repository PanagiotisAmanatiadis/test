/**
 * @file ex06_sales_analysis.cpp
 * @brief Computes sales revenue per salesman and units sold per product,
 *        then identifies the best performer and best-selling product.
 *
 * Data is hardcoded (4 salesmen × 5 products) as per the original exercise.
 */

#include <algorithm>
#include <array>
#include <iostream>

namespace {
    constexpr int SALESMEN = 4;
    constexpr int PRODUCTS = 5;

    constexpr std::array<int, PRODUCTS> PRICE_PER_PRODUCT{250, 150, 320, 210, 920};

    constexpr std::array<std::array<int, PRODUCTS>, SALESMEN> SALES{{
        {10,  4,  5,  6,  7},
        { 7,  0, 12,  1,  3},
        { 4, 19,  5,  0,  8},
        { 3,  2,  1,  5,  6}
    }};
} // namespace

/**
 * @brief Computes total revenue per salesman.
 * @return Array of per-salesman revenue totals.
 */
[[nodiscard]] std::array<int, SALESMEN> computeSalesmanRevenue() {
    std::array<int, SALESMEN> revenue{};
    for (int i = 0; i < SALESMEN; ++i) {
        for (int j = 0; j < PRODUCTS; ++j) {
            revenue[i] += SALES[i][j] * PRICE_PER_PRODUCT[j];
        }
    }
    return revenue;
}

/**
 * @brief Computes total units sold per product.
 * @return Array of per-product unit totals.
 */
[[nodiscard]] std::array<int, PRODUCTS> computeProductUnits() {
    std::array<int, PRODUCTS> units{};
    for (int i = 0; i < SALESMEN; ++i) {
        for (int j = 0; j < PRODUCTS; ++j) {
            units[j] += SALES[i][j];
        }
    }
    return units;
}

/**
 * @brief Prints an indexed array with the index of the maximum element.
 * @param label     Row label.
 * @param unitLabel Column value label.
 * @param data      Array of integer values.
 */
template <std::size_t N>
void printWithBest(const std::string& label, const std::string& unitLabel,
                   const std::array<int, N>& data) {
    std::cout << label << "-" << unitLabel << '\n';
    for (std::size_t i = 0; i < N; ++i) {
        std::cout << "  " << i << "      " << data[i] << '\n';
    }
    const auto bestIdx = std::max_element(data.cbegin(), data.cend()) - data.cbegin();
    std::cout << "Best " << label << " was " << bestIdx
              << " with " << data[bestIdx] << " " << unitLabel << '\n';
}

int main() {
    const auto revenue = computeSalesmanRevenue();
    const auto units   = computeProductUnits();

    printWithBest("SalesMan", "Sales",  revenue);
    printWithBest("Product",  "Items",  units);

    return 0;
}
