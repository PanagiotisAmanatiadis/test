/**
 * @file ex02_product_discount.cpp
 * @brief Computes final order price with a quantity-based discount.
 *
 * The product price is derived from its code (first two digits).
 * Discount tiers: ≤30 units → 10%, ≤70 → 20%, >70 → 35%.
 */

#include <cmath>
#include <iomanip>
#include <iostream>

/**
 * @brief Extracts the price from a product code (first two significant digits).
 * @param code  Product code integer.
 * @return Unit price.
 */
[[nodiscard]] int priceFromCode(int code) {
    if (code < 10) {
        return code;  // single digit: price equals code
    }
    const int digits = static_cast<int>(std::ceil(std::log10(static_cast<double>(code))));
    return code / static_cast<int>(std::pow(10.0, digits - 2));
}

/**
 * @brief Computes gross order total (quantity × price).
 * @param quantity  Number of units ordered.
 * @param unitPrice Unit price.
 * @return Gross total.
 */
[[nodiscard]] double grossTotal(int quantity, int unitPrice) {
    return static_cast<double>(quantity) * unitPrice;
}

/**
 * @brief Computes the discount amount based on quantity tier.
 * @param quantity  Number of units ordered.
 * @param unitPrice Unit price.
 * @return Discount amount.
 */
[[nodiscard]] double discountAmount(int quantity, int unitPrice) {
    const double rate = (quantity <= 30) ? 0.10
                      : (quantity <= 70) ? 0.20
                                         : 0.35;
    return grossTotal(quantity, unitPrice) * rate;
}

int main() {
    int productCode{}, quantity{};

    std::cout << "Enter product code:      ";
    std::cin >> productCode;
    std::cout << "Enter quantity (units):  ";
    std::cin >> quantity;

    const int    price    = priceFromCode(productCode);
    const double discount = discountAmount(quantity, price);
    const double final_   = grossTotal(quantity, price) - discount;

    std::cout << std::fixed << std::setprecision(2)
              << "Unit price:    " << price    << '\n'
              << "Discount:      " << discount << '\n'
              << "Final total:   " << final_   << '\n';
    return 0;
}
