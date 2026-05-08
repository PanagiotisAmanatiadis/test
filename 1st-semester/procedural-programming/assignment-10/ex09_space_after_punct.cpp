/**
 * @file ex09_space_after_punct.cpp
 * @brief Reads i10f9.dat and writes i10f9.dat's content to o10f9.dat,
 *        inserting a space before any non-whitespace character that
 *        immediately follows a '.' or ','.
 */

#include <fstream>
#include <iostream>

#include "../include/Logger.hpp"

int main() {
    std::ifstream inFile("i10f9.dat");
    std::ofstream outFile("o10f9.dat");

    if (!inFile.is_open()) { Logger::error("Cannot open i10f9.dat"); return 1; }
    if (!outFile.is_open()) { Logger::error("Cannot open o10f9.dat"); return 1; }

    bool afterPunct = false;
    char ch{};

    while (inFile.get(ch)) {
        if (afterPunct && ch != ' ' && ch != '\n' && ch != '\r') {
            outFile.put(' ');
        }
        outFile.put(ch);
        afterPunct = (ch == '.' || ch == ',');
    }

    Logger::info("Output written to o10f9.dat");
    return 0;
}
