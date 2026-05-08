/**
 * @file ex01_property_tax.cpp
 * @brief Computes property transfer tax (DT) and stamp duty (DF) for a
 *        property based on its net and gross square metres.
 *
 * Formulas (for a 2-month reference period of 61/365 years):
 *   DT = net_sqm  × 1.33 × (61/365)
 *   DF = gross_sqm × 0.13 × (61/365)
 */

#include <iomanip>
#include <iostream>

namespace {
    constexpr double TWO_MONTHS = 61.0 / 365.0;
}

/** @brief Holds computed tax results for a property. */
struct PropertyTax {
    double dt{};  ///< Transfer tax
    double df{};  ///< Stamp duty
};

/**
 * @brief Computes property taxes from square-metre areas.
 * @param netSqm    Net (interior) area in m².
 * @param grossSqm  Gross area in m².
 * @return PropertyTax with dt and df fields populated.
 */
[[nodiscard]] PropertyTax calculateTax(unsigned long netSqm, unsigned long grossSqm) {
    return {
        static_cast<double>(netSqm)   * 1.33 * TWO_MONTHS,
        static_cast<double>(grossSqm) * 0.13 * TWO_MONTHS
    };
}

int main() {
    unsigned long netSqm{}, grossSqm{};

    std::cout << "Enter net area (m²):   ";
    std::cin >> netSqm;
    std::cout << "Enter gross area (m²): ";
    std::cin >> grossSqm;

    const auto tax = calculateTax(netSqm, grossSqm);

    std::cout << std::fixed << std::setprecision(2)
              << "Transfer tax (DT): " << tax.dt << '\n'
              << "Stamp duty   (DF): " << tax.df << '\n';
    return 0;
}
