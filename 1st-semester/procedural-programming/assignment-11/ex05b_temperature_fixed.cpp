/**
 * @file ex05b_temperature_fixed.cpp
 * @brief Corrected version of ex05_temperature_data.cpp.
 *
 * Fix: the max-deviation loop now tests each sample (city[j]) against the
 * national average instead of always using city[0].
 */

#include <algorithm>
#include <cmath>
#include <iostream>
#include <numeric>
#include <vector>

namespace {
    constexpr int CITIES          = 10;
    constexpr int SAMPLES_PER_DAY = 3;
}

/**
 * @brief Reads temperature samples from stdin into a 2-D vector.
 * @return cities × samplesPerDay matrix of temperatures.
 */
[[nodiscard]] std::vector<std::vector<double>> readTemperatures() {
    std::vector<std::vector<double>> data(CITIES, std::vector<double>(SAMPLES_PER_DAY));
    for (auto& city : data) {
        for (auto& sample : city) {
            std::cin >> sample;
        }
    }
    return data;
}

/**
 * @brief Computes the maximum absolute deviation of city samples from a reference.
 * @param cityTemps  Temperature samples for one city.
 * @param reference  Value to compare against (national average).
 * @return Maximum |sample − reference| across all samples.
 */
[[nodiscard]] double maxDeviation(const std::vector<double>& cityTemps, double reference) {
    double maxDev{};
    for (const auto t : cityTemps) {
        maxDev = std::max(maxDev, std::fabs(t - reference));
    }
    return maxDev;
}

int main() {
    const auto data = readTemperatures();

    std::vector<double> flat;
    flat.reserve(CITIES * SAMPLES_PER_DAY);
    for (const auto& city : data) {
        for (const auto t : city) {
            flat.push_back(t);
        }
    }
    const double nationalAvg = std::accumulate(flat.cbegin(), flat.cend(), 0.0)
                               / static_cast<double>(flat.size());
    std::cout << "National average: " << nationalAvg << '\n';

    for (const auto& city : data) {
        const double localAvg = std::accumulate(city.cbegin(), city.cend(), 0.0)
                                / static_cast<double>(SAMPLES_PER_DAY);
        std::cout << localAvg << ' ' << maxDeviation(city, nationalAvg) << '\n';
    }
    return 0;
}
