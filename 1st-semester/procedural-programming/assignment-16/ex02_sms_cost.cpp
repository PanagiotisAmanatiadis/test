/**
 * @file ex02_sms_cost.cpp
 * @brief Calculates the total cost of sending N SMS messages using a
 *        tiered pricing model.
 *
 * Pricing tiers (in euro cents per SMS):
 *   First 10  messages: 2.0 ¢
 *   Next  50  messages: 1.5 ¢
 *   Next  100 messages: 1.2 ¢
 *   Above 160 messages: 1.0 ¢
 * Result is reported in euros.
 */

#include <iomanip>
#include <iostream>

/**
 * @brief Computes the total SMS cost in euros for the given message count.
 * @param count  Number of SMS messages sent.
 * @return Total cost in euros.
 */
[[nodiscard]] double smsCost(int count) {
    double cents{};
    if (count > 160) {
        cents = 10 * 2.0 + 50 * 1.5 + 100 * 1.2 + (count - 160) * 1.0;
    } else if (count > 60) {
        cents = 10 * 2.0 + 50 * 1.5 + (count - 60) * 1.2;
    } else if (count > 10) {
        cents = 10 * 2.0 + (count - 10) * 1.5;
    } else {
        cents = count * 2.0;
    }
    return cents / 100.0;
}

int main() {
    int count{};
    std::cout << "Enter number of SMS messages: ";
    std::cin >> count;

    std::cout << std::fixed << std::setprecision(2)
              << "Total cost: " << smsCost(count) << " EUR\n";
    return 0;
}
