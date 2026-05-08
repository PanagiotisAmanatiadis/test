/**
 * @file ex08_car_rental.cpp
 * @brief Manages a collection of car rental records, computes total revenue,
 *        and identifies the highest-value rental.
 */

#include <algorithm>
#include <iomanip>
#include <iostream>
#include <string>
#include <vector>

/** @brief Represents a single car rental record. */
struct CarRental {
    int         id{};
    std::string brand;
    unsigned int cc{};
    std::string  customerName;
    unsigned int rentDays{};
    double       dailyRate{};

    /** @brief Computes total rental price for this record. */
    [[nodiscard]] double totalPrice() const {
        return static_cast<double>(rentDays) * dailyRate;
    }
};

/**
 * @brief Reads a single CarRental record from stdin.
 * @param id  Sequential identifier to assign to the record.
 * @return Populated CarRental.
 */
[[nodiscard]] CarRental readCarRental(int id) {
    CarRental cr;
    cr.id = id;
    std::cout << "Brand:        "; std::cin.ignore(); std::getline(std::cin, cr.brand);
    std::cout << "Engine (cc):  "; std::cin >> cr.cc;
    std::cout << "Customer:     "; std::cin.ignore(); std::getline(std::cin, cr.customerName);
    std::cout << "Rental days:  "; std::cin >> cr.rentDays;
    std::cout << "Daily rate:   "; std::cin >> cr.dailyRate;
    return cr;
}

/**
 * @brief Prints a formatted row for one rental record.
 * @param cr     The rental record.
 * @param price  Pre-computed total price.
 */
void printRental(const CarRental& cr, double price) {
    std::cout << std::left
              << std::setw(8)  << cr.id
              << std::setw(22) << cr.customerName
              << std::setw(12) << cr.brand
              << std::setw(6)  << cr.cc
              << std::setw(6)  << cr.rentDays
              << std::fixed << std::setprecision(2)
              << std::setw(8)  << cr.dailyRate
              << price << '\n';
}

int main() {
    int count{};
    std::cout << "Number of rentals: ";
    std::cin >> count;

    std::vector<CarRental> rentals;
    rentals.reserve(static_cast<size_t>(count));

    for (int i = 0; i < count; ++i) {
        std::cout << "\n--- Rental " << i + 1 << " ---\n";
        rentals.push_back(readCarRental(i));
    }

    const auto bestIt = std::max_element(rentals.cbegin(), rentals.cend(),
        [](const CarRental& a, const CarRental& b) {
            return a.totalPrice() < b.totalPrice();
        });

    double totalRevenue{};
    for (const auto& r : rentals) {
        totalRevenue += r.totalPrice();
    }

    std::cout << "\nNumber  Name                 Type        CC    Days  Price   Total\n"
              << std::string(72, '-') << '\n';
    for (const auto& r : rentals) {
        printRental(r, r.totalPrice());
    }
    std::cout << std::string(72, '-') << '\n'
              << std::fixed << std::setprecision(2)
              << std::setw(60) << "Grand total:" << "  " << totalRevenue << '\n';

    if (bestIt != rentals.cend()) {
        std::cout << "Best rental: " << bestIt->brand
                  << " (" << bestIt->cc << " cc)"
                  << " for " << bestIt->totalPrice() << " EUR\n";
    }
    return 0;
}
