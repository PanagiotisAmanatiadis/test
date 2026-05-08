/**
 * @file ex09_student_absences.cpp
 * @brief Reads student absence data from a CSV file and writes a formatted
 *        report of students exceeding 100 absences to an output file.
 *
 * Input CSV format per line:  name, absences, comments
 */

#include <fstream>
#include <iomanip>
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

#include "../include/Logger.hpp"

/** @brief Holds a single student's name and absence count. */
struct Student {
    std::string name;
    int absences{};
};

/**
 * @brief Prompts the user for a file path.
 * @param purpose Human-readable description of the file's role.
 * @return The path string entered by the user.
 */
[[nodiscard]] std::string promptFilePath(const std::string& purpose) {
    std::string path;
    std::cout << "Enter filename for " << purpose << ": ";
    std::cin >> path;
    return path;
}

/**
 * @brief Reads students with absences > 100 from the given CSV file.
 *
 * @param inPath         Path to the input file.
 * @param totalStudents  Output: total number of student records read.
 * @return Vector of students whose absences exceed 100.
 * @throws std::runtime_error if the file cannot be opened.
 */
[[nodiscard]] std::vector<Student> readAbsentStudents(const std::string& inPath,
                                                      int& totalStudents) {
    std::ifstream inFile(inPath);
    if (!inFile.is_open()) {
        throw std::runtime_error("Cannot open input file: " + inPath);
    }

    std::vector<Student> absent;
    totalStudents = 0;
    std::string line;
    int lineNum{};

    while (std::getline(inFile, line)) {
        ++lineNum;
        const auto firstComma = line.find(',');
        if (firstComma == std::string::npos) {
            Logger::warning("Parse error at line " + std::to_string(lineNum) + ". Skipping.");
            continue;
        }
        const std::string name = line.substr(0, firstComma);
        std::istringstream rest(line.substr(firstComma + 1));
        int absences{};
        if (!(rest >> absences)) {
            Logger::warning("Parse error at line " + std::to_string(lineNum) + ". Skipping.");
            continue;
        }
        ++totalStudents;
        if (absences > 100) {
            absent.push_back({name, absences});
        }
    }
    return absent;
}

/**
 * @brief Writes the absence report to an output file.
 *
 * @param outPath        Path to the output file.
 * @param absent         Students with absences > 100.
 * @param totalStudents  Total number of students in the input.
 * @throws std::runtime_error if the output file cannot be opened.
 */
void writeReport(const std::string& outPath,
                 const std::vector<Student>& absent,
                 int totalStudents) {
    std::ofstream outFile(outPath);
    if (!outFile.is_open()) {
        throw std::runtime_error("Cannot open output file: " + outPath);
    }

    constexpr int nameWidth = 30;
    outFile << std::left
            << std::setw(nameWidth) << "NAME" << "ABSENCES\n"
            << std::string(39, '-') << '\n';

    for (const auto& s : absent) {
        outFile << std::setw(nameWidth) << s.name << s.absences << '\n';
    }

    outFile << std::string(39, '-') << '\n'
            << std::setw(nameWidth) << "TOTAL STUDENTS:" << totalStudents    << '\n'
            << std::setw(nameWidth) << "TOTAL ABSENT:"   << absent.size()    << '\n';
}

int main() {
    try {
        const std::string inPath  = promptFilePath("input");
        const std::string outPath = promptFilePath("output");
        int totalStudents{};
        const auto absent = readAbsentStudents(inPath, totalStudents);
        writeReport(outPath, absent, totalStudents);
        Logger::info("Report written to " + outPath);
    } catch (const std::exception& e) {
        Logger::error(e.what());
        return 1;
    }
    return 0;
}
