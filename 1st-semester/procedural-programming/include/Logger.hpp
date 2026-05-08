#pragma once

#include <iostream>
#include <string>

/**
 * @brief Lightweight severity-levelled logger.
 *
 * INFO writes to stdout; WARN and ERROR write to stderr.
 * All methods are static — no instantiation required.
 */
class Logger {
public:
    /** @brief Logs an informational message to stdout. */
    static void info(const std::string& msg) {
        std::cout << "[INFO]  " << msg << '\n';
    }

    /** @brief Logs a warning to stderr. */
    static void warning(const std::string& msg) {
        std::cerr << "[WARN]  " << msg << '\n';
    }

    /** @brief Logs an error to stderr. */
    static void error(const std::string& msg) {
        std::cerr << "[ERROR] " << msg << '\n';
    }
};
