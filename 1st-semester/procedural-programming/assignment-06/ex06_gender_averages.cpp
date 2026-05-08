/**
 * @file ex06_gender_averages.cpp
 * @brief Reads demographic data for N individuals and computes average
 *        weight, height, and age grouped by gender.
 *
 * Gender encoding: 1 = male, 2 = female.
 * Gender index used internally: gender % 2  (1→1 = male, 2→0 = female).
 */

#include <array>
#include <iostream>
#include <string>
#include <vector>

/** @brief Holds one individual's demographic measurements. */
struct Person {
    int gender{};  ///< 1 = male, 2 = female
    int weight{};  ///< kilograms
    int height{};  ///< centimetres
    int age{};
};

/**
 * @brief Reads N persons from stdin.
 * @param n Number of persons to read.
 * @return Vector of Person structs.
 */
[[nodiscard]] std::vector<Person> readPersons(int n) {
    std::vector<Person> persons(static_cast<size_t>(n));
    for (int i = 0; i < n; ++i) {
        std::cout << "--- Person " << i + 1 << " ---\n";
        std::cout << "Gender (1=M, 2=F): "; std::cin >> persons[i].gender;
        std::cout << "Weight (kg):       "; std::cin >> persons[i].weight;
        std::cout << "Height (cm):       "; std::cin >> persons[i].height;
        std::cout << "Age:               "; std::cin >> persons[i].age;
    }
    return persons;
}

/**
 * @brief Computes gender-split averages for a single field.
 * @param persons    All individuals.
 * @param fieldIdx   0 = weight, 1 = height, 2 = age.
 * @return {maleAvg, femaleAvg} — index mirrors gender%2 (1=male, 0=female).
 */
[[nodiscard]] std::array<double, 2> computeAverages(const std::vector<Person>& persons,
                                                    int fieldIdx) {
    std::array<double, 2> sums{};
    std::array<int, 2>    counts{};

    for (const auto& p : persons) {
        const int g = p.gender % 2;  // 1→male slot, 0→female slot
        ++counts[g];
        const int value = (fieldIdx == 0) ? p.weight
                        : (fieldIdx == 1) ? p.height
                                          : p.age;
        sums[g] += value;
    }
    return {counts[0] ? sums[0] / counts[0] : 0.0,
            counts[1] ? sums[1] / counts[1] : 0.0};
}

int main() {
    int n{};
    std::cout << "Enter number of persons: ";
    std::cin >> n;

    const auto persons = readPersons(n);

    static const std::array<std::string, 3> labels{"weight", "height", "age"};
    // index 0 = female (gender%2==0), index 1 = male (gender%2==1)
    static const std::array<std::string, 2> genderLabels{"female", "male"};

    for (int field = 0; field < 3; ++field) {
        const auto avgs = computeAverages(persons, field);
        for (int g = 0; g < 2; ++g) {
            std::cout << "Average " << labels[field]
                      << " (" << genderLabels[g] << "): " << avgs[g] << '\n';
        }
        std::cout << '\n';
    }
    return 0;
}
