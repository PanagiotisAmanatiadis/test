/**
 * @file ex05_temperature_data.cpp
 * @brief Reads temperature samples for 10 cities (3 per city), computes the
 *        national average, and for each city reports local average and max
 *        deviation from the national average.
 *
 * @note This is the original version of the exercise. A corrected version
 *       (ex05b_temperature_fixed.cpp) fixes the max-deviation loop bug present
 *       in the original source.
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

int main() {
    const auto data = readTemperatures();

    // Flatten to compute national average
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

        // Original: only checks city[0] against nationalAvg in every iteration (preserved as-is)
        double maxDev = std::fabs(city[0] - nationalAvg);
        for (int j = 1; j < SAMPLES_PER_DAY; ++j) {
            const double d = std::fabs(city[0] - nationalAvg);  // original bug: always city[0]
            if (d > maxDev) maxDev = d;
        }

        std::cout << localAvg << ' ' << maxDev << '\n';
    }
    return 0;
}
