/**
 * @file ex07_email_parser.cpp
 * @brief Reads an email address, trims surrounding whitespace, then
 *        extracts and prints the local-part (before @) and the domain
 *        (after @).
 */

#include <algorithm>
#include <cctype>
#include <iostream>
#include <stdexcept>
#include <string>

/**
 * @brief Trims leading and trailing whitespace from a string.
 * @param s The string to trim.
 * @return Trimmed copy.
 */
[[nodiscard]] std::string trim(std::string s) {
    const auto notSpace = [](unsigned char c) { return !std::isspace(c); };
    s.erase(s.begin(), std::find_if(s.begin(), s.end(), notSpace));
    s.erase(std::find_if(s.rbegin(), s.rend(), notSpace).base(), s.end());
    return s;
}

int main() {
    std::cout << "Enter an email address: ";
    std::string raw;
    std::getline(std::cin, raw);

    const std::string address = trim(raw);
    std::cout << "Trimmed address: " << address << '\n';

    const auto atPos = address.find('@');
    if (atPos == std::string::npos) {
        std::cerr << "Error: no '@' found in address.\n";
        return 1;
    }

    const std::string localPart = address.substr(0, atPos);
    const std::string domain    = address.substr(atPos + 1);

    std::cout << "Local part: " << localPart << '\n'
              << "Local part length: " << localPart.size() << '\n'
              << "Domain: " << domain << '\n';
    return 0;
}
