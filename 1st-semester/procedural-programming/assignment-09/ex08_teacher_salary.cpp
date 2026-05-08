/**
 * @file ex08_teacher_salary.cpp
 * @brief Reads hourly rate and hours worked for N teachers and prints a
 *        formatted payroll table with gross pay, deductions, tax, and net pay.
 *
 * Deductions: 15% of gross.
 * Tax: 7% of (gross − deductions).
 * Net: gross − deductions − tax.
 */

#include <iomanip>
#include <iostream>
#include <string>
#include <vector>

/** @brief Holds one teacher's identity and computed pay components. */
struct Teacher {
    std::string name;
    std::string surname;
    double      wage{};
    int         hours{};
    double      gross{};
    double      deductions{};
    double      tax{};
    double      net{};

    /** @brief Populates the computed salary fields from wage and hours. */
    void computeSalary() {
        gross      = wage * static_cast<double>(hours);
        deductions = gross * 0.15;
        tax        = (gross - deductions) * 0.07;
        net        = gross - deductions - tax;
    }
};

/**
 * @brief Reads one Teacher record from stdin.
 * @return Populated Teacher with salary computed.
 */
[[nodiscard]] Teacher readTeacher() {
    Teacher t;
    std::cout << "First name:   "; std::getline(std::cin, t.name);
    std::cout << "Last name:    "; std::getline(std::cin, t.surname);
    std::cout << "Hourly rate:  "; std::cin >> t.wage;
    std::cout << "Hours worked: "; std::cin >> t.hours;
    std::cin.ignore();
    t.computeSalary();
    return t;
}

int main() {
    int n{};
    std::cout << "Number of teachers: ";
    std::cin >> n;
    std::cin.ignore();

    std::vector<Teacher> teachers;
    teachers.reserve(static_cast<size_t>(n));

    for (int i = 0; i < n; ++i) {
        std::cout << "\n--- Teacher " << i + 1 << " ---\n";
        teachers.push_back(readTeacher());
    }

    std::cout << "\n\n"
              << std::left
              << std::setw(16) << "Name"
              << std::setw(21) << "Surname"
              << std::setw(13) << "Hourly Rate"
              << std::setw(14) << "Hours Worked"
              << std::setw(9)  << "Gross"
              << std::setw(12) << "Deductions"
              << std::setw(8)  << "Tax"
              << "Net\n"
              << std::string(101, '-') << '\n';

    std::cout << std::fixed << std::setprecision(2);
    for (const auto& t : teachers) {
        std::cout << std::left
                  << std::setw(16) << t.name
                  << std::setw(21) << t.surname
                  << std::setw(13) << t.wage
                  << std::setw(14) << t.hours
                  << std::setw(9)  << t.gross
                  << std::setw(12) << t.deductions
                  << std::setw(8)  << t.tax
                  << t.net << '\n';
    }
    return 0;
}
