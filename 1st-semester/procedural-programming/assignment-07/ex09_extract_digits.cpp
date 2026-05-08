/**
 * @file ex09_extract_digits.cpp
 * @brief Reads i7f9.dat character by character and writes each contiguous
 *        sequence of digit characters to a separate line in o7f9.dat.
 */

#include <cctype>
#include <fstream>
#include <iostream>

#include "../include/Logger.hpp"

int main() {
    std::ifstream inFile("i7f9.dat");
    std::ofstream outFile("o7f9.dat");

    if (!inFile.is_open()) { Logger::error("Cannot open i7f9.dat"); return 1; }
    if (!outFile.is_open()) { Logger::error("Cannot open o7f9.dat"); return 1; }

    bool insideNumber = false;
    char ch{};

    while (inFile.get(ch)) {
        if (std::isdigit(static_cast<unsigned char>(ch))) {
            outFile.put(ch);
            insideNumber = true;
        } else if (insideNumber) {
            outFile.put('\n');
            insideNumber = false;
        }
    }

    Logger::info("Digit sequences written to o7f9.dat");
    return 0;
}
