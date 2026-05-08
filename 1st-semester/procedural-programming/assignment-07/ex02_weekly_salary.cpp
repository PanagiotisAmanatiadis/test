/**
 * @file ex02_weekly_salary.cpp
 * @brief Calculates weekly salary based on employee type.
 *
 * Employees with code < 1000 are hourly workers (overtime applies for
 * hours > 40). Employees with code >= 1000 are salaried workers paid
 * an annual salary divided by 52 weeks.
 */

#include <iomanip>
#include <iostream>

/**
 * @brief Computes weekly pay for an hourly worker.
 *
 * Hours beyond 40 are paid at double the hourly rate (base + overtime).
 *
 * @param hours  Hours worked in the week.
 * @param wage   Hourly wage rate.
 * @return Weekly pay amount.
 */
[[nodiscard]] double weeklyPayByWage(int hours, double wage) {
    double pay = static_cast<double>(hours) * wage;
    if (hours > 40) {
        pay += static_cast<double>(hours - 40) * wage;  // overtime bonus
    }
    return pay;
}

/**
 * @brief Computes weekly pay for a salaried worker.
 * @param annualSalary  Gross annual salary.
 * @return Weekly pay (annual / 52).
 */
[[nodiscard]] double weeklyPayByYear(double annualSalary) {
    return annualSalary / 52.0;
}

int main() {
    long employeeCode{};
    std::cout << "Enter employee code: ";
    std::cin >> employeeCode;

    double weeklySalary{};

    if (employeeCode < 1000) {
        int hours{};
        double wage{};
        std::cout << "Enter hours worked this week: ";
        std::cin >> hours;
        std::cout << "Enter hourly wage: ";
        std::cin >> wage;
        weeklySalary = weeklyPayByWage(hours, wage);
    } else {
        double annualSalary{};
        std::cout << "Enter annual salary: ";
        std::cin >> annualSalary;
        weeklySalary = weeklyPayByYear(annualSalary);
    }

    std::cout << std::fixed << std::setprecision(2)
              << "Weekly pay: " << weeklySalary << '\n';
    return 0;
}
