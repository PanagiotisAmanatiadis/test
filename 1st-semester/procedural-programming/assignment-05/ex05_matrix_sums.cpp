/**
 * @file ex05_matrix_sums.cpp
 * @brief Reads a user-defined matrix and reports row sums, column sums,
 *        and diagonal sums (for square matrices).
 *
 * Replaces heap-allocated C arrays and raw pointer arithmetic with
 * std::vector<std::vector<long>>.
 */

#include <iomanip>
#include <iostream>
#include <vector>

/**
 * @brief Reads a rows × columns matrix of long integers from stdin.
 * @param rows     Number of rows.
 * @param columns  Number of columns.
 * @return 2-D vector populated with user input.
 */
[[nodiscard]] std::vector<std::vector<long>> readMatrix(int rows, int columns) {
    std::vector<std::vector<long>> matrix(rows, std::vector<long>(columns));
    for (int i = 0; i < rows; ++i) {
        for (int j = 0; j < columns; ++j) {
            std::cout << "Position [" << i << ',' << j << "]: ";
            std::cin >> matrix[i][j];
        }
    }
    return matrix;
}

int main() {
    int rows{}, columns{};
    std::cout << "Enter number of rows: ";
    std::cin >> rows;
    std::cout << "Enter number of columns: ";
    std::cin >> columns;

    const auto matrix = readMatrix(rows, columns);
    std::vector<long> colSum(static_cast<size_t>(columns), 0L);

    std::cout << "\nTable:\n";
    for (int i = 0; i < rows; ++i) {
        long rowSum{};
        for (int j = 0; j < columns; ++j) {
            rowSum     += matrix[i][j];
            colSum[j]  += matrix[i][j];
            std::cout << std::setw(4) << matrix[i][j];
        }
        std::cout << "| = " << rowSum << '\n';
    }

    std::cout << std::string(static_cast<size_t>(columns) * 4, '-') << '\n';
    for (const auto s : colSum) {
        std::cout << std::setw(4) << s;
    }
    std::cout << '\n';

    if (rows == columns) {
        long diagMain{}, diagAnti{};
        for (int i = 0; i < rows; ++i) {
            diagMain += matrix[i][i];
            diagAnti += matrix[i][columns - i - 1];
        }
        std::cout << "Main diagonal sum: " << diagMain
                  << ",  Anti-diagonal sum: " << diagAnti << '\n';
    }
    return 0;
}
