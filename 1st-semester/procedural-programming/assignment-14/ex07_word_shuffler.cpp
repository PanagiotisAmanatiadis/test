/**
 * @file ex07_word_shuffler.cpp
 * @brief Reads a word from stdin and prints a randomly shuffled copy.
 *
 * Uses the Fisher-Yates (Knuth) shuffle algorithm via std::shuffle
 * with a Mersenne Twister PRNG.
 */

#include <algorithm>
#include <iostream>
#include <random>
#include <string>

/**
 * @brief Returns a shuffled copy of the input string.
 * @param word  The original string.
 * @return Shuffled copy.
 */
[[nodiscard]] std::string shuffled(std::string word) {
    std::mt19937 rng{std::random_device{}()};
    std::shuffle(word.begin(), word.end(), rng);
    return word;
}

int main() {
    std::cout << "Enter a word to shuffle: ";
    std::string word;
    std::getline(std::cin, word);

    std::cout << "Original: " << word         << '\n'
              << "Shuffled: " << shuffled(word) << '\n';
    return 0;
}
