/**
 * @file ex05_random_matrix.cpp
 * @brief Generates a random integer matrix, then for each row finds the
 *        maximum element and sets all elements up to and including that
 *        position equal to the maximum.
 */

#include <algorithm>
#include <cstdlib>
#include <ctime>
#include <iomanip>
#include <iostream>
#include <vector>

/**
 * @brief Fills a rows × columns matrix with random integers in [0, 99].
 * @param rows     Number of rows.
 * @param columns  Number of columns.
 * @return Populated 2-D vector.
 */
[[nodiscard]] std::vector<std::vector<int>> randomMatrix(int rows, int columns) {
    std::vector<std::vector<int>> m(static_cast<size_t>(rows),
                                    std::vector<int>(static_cast<size_t>(columns)));
    for (auto& row : m) {
        for (auto& cell : row) {
            cell = std::rand() / (RAND_MAX / 100 + 1);
        }
    }
    return m;
}

/**
 * @brief In a single row, finds the max element and sets all elements from
 *        index 0 up to (and including) the max's position equal to the max.
 * @param row  The row vector to transform in-place.
 */
void applyRowTransform(std::vector<int>& row) {
    const auto maxIt  = std::max_element(row.begin(), row.end());
    const int  maxVal = *maxIt;
    const auto maxPos = maxIt - row.begin();
    for (auto it = row.begin(); it <= maxIt; ++it) {
        *it = maxVal;
    }
    (void)maxPos;  // maxPos used implicitly through iterator range
}

/**
 * @brief Prints a matrix with fixed-width cells.
 * @param m  Matrix to print.
 */
void printMatrix(const std::vector<std::vector<int>>& m) {
    for (const auto& row : m) {
        for (const auto v : row) {
            std::cout << std::setw(3) << v << ' ';
        }
        std::cout << '\n';
    }
}

int main() {
    std::srand(static_cast<unsigned>(std::time(nullptr)));

    int rows{}, columns{};
    std::cout << "Enter number of rows:    ";
    std::cin >> rows;
    std::cout << "Enter number of columns: ";
    std::cin >> columns;

    auto matrix = randomMatrix(rows, columns);

    std::cout << "\nOriginal matrix:\n";
    printMatrix(matrix);

    for (auto& row : matrix) {
        applyRowTransform(row);
    }

    std::cout << "\nTransformed matrix:\n";
    printMatrix(matrix);

    return 0;
}
