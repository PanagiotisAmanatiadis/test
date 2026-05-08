/**
 * @file ex09_kickback_report.cpp
 * @brief Reads product records from i4f9.dat and writes a kickback report
 *        to o4f9.dat.
 *
 * Each input record format:  code,name,price\n
 * Kickback rates by code: 11 → 3%, 12 → 5%, 13 → 8%, 14 → 11%, other → 100%.
 */

#include <fstream>
#include <iomanip>
#include <iostream>
#include <string>

#include "../include/Logger.hpp"

/**
 * @brief Returns the kickback amount for a given category code and price.
 * @param code   Product category code (11–14).
 * @param price  Product price.
 * @return Kickback amount as a long.
 */
[[nodiscard]] long computeKickback(int code, long price) {
    double rate{};
    switch (code) {
        case 11: rate = 0.03; break;
        case 12: rate = 0.05; break;
        case 13: rate = 0.08; break;
        case 14: rate = 0.11; break;
        default: rate = 1.00; break;
    }
    return static_cast<long>(static_cast<double>(price) * rate);
}

int main() {
    std::ifstream inFile("i4f9.dat");
    std::ofstream outFile("o4f9.dat");

    if (!inFile.is_open()) { Logger::error("Cannot open i4f9.dat"); return 1; }
    if (!outFile.is_open()) { Logger::error("Cannot open o4f9.dat"); return 1; }

    int code{};
    int lineNum{};

    while (inFile >> code) {
        ++lineNum;
        char comma{};
        inFile >> comma;

        std::string name;
        if (!std::getline(inFile, name, ',')) {
            Logger::warning("Format error at line " + std::to_string(lineNum) + ". Skipping.");
            continue;
        }
        long price{};
        if (!(inFile >> price)) {
            Logger::warning("Format error at line " + std::to_string(lineNum) + ". Skipping.");
            continue;
        }
        inFile.ignore(); // consume newline

        outFile << std::left << std::setw(25) << name
                << std::left << std::setw(6)  << computeKickback(code, price) << '\n';
    }

    Logger::info("Report written to o4f9.dat");
    return 0;
}
