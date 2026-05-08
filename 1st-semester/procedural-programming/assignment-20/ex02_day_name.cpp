/**
 * @file ex02_day_name.cpp
 * @brief Reads an integer in [1, 7] and prints the corresponding day name.
 */

#include <array>
#include <iostream>
#include <stdexcept>
#include <string_view>

/**
 * @brief Returns the day name for a number in [1, 7].
 * @param num  Day number (1 = Monday … 7 = Sunday).
 * @return Name of the day.
 * @throws std::out_of_range if num is not in [1, 7].
 */
[[nodiscard]] std::string_view dayName(int num) {
    static constexpr std::array<std::string_view, 7> DAYS{
        "Monday", "Tuesday", "Wednesday", "Thursday",
        "Friday", "Saturday", "Sunday"
    };
    if (num < 1 || num > 7) {
        throw std::out_of_range("Day number must be between 1 and 7.");
    }
    return DAYS[static_cast<size_t>(num - 1)];
}

int main() {
    int num{};
    std::cout << "Enter a number from 1 to 7: ";
    std::cin >> num;

    try {
        std::cout << "The day is " << dayName(num) << '\n';
    } catch (const std::out_of_range& e) {
        std::cerr << "Error: " << e.what() << '\n';
        return 1;
    }
    return 0;
}
