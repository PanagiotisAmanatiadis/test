/**
 * @file ex04_vat_calculator.cpp
 * @brief Reads 5 products (quantity, price, VAT category) and reports
 *        total order cost and total VAT.
 *
 * VAT categories:
 *   1 → 0%  (exempt)
 *   2 → 6%
 *   3 → 13%
 *   4 → 19%
 */

#include <iomanip>
#include <iostream>
#include <optional>

/**
 * @brief Maps a VAT category code to its rate.
 * @param category  Category code (1–4).
 * @return VAT rate as a fraction, or std::nullopt for an invalid code.
 */
[[nodiscard]] std::optional<float> vatRate(int category) {
    switch (category) {
        case 1: return 0.00f;
        case 2: return 0.06f;
        case 3: return 0.13f;
        case 4: return 0.19f;
        default: return std::nullopt;
    }
}

int main() {
    constexpr int NUM_PRODUCTS = 5;

    int   totalPrice{};
    float totalVAT{};

    for (int i = 1; i <= NUM_PRODUCTS; ++i) {
        int quantity{}, pricePerUnit{}, category{};

        std::cout << "--- Product " << i << " ---\n";
        std::cout << "Quantity:     "; std::cin >> quantity;
        std::cout << "Unit price:   "; std::cin >> pricePerUnit;
        std::cout << "VAT category: "; std::cin >> category;

        const auto rate = vatRate(category);
        if (!rate.has_value()) {
            std::cerr << "Invalid VAT category " << category << ". Skipping.\n";
            continue;
        }

        const int lineTotal = pricePerUnit * quantity;
        totalPrice += lineTotal;
        totalVAT   += static_cast<float>(lineTotal) * *rate;
    }

    std::cout << std::fixed << std::setprecision(2)
              << "Total cost (incl. VAT): " << static_cast<float>(totalPrice) + totalVAT << '\n'
              << "Total VAT:              " << totalVAT << '\n';
    return 0;
}
