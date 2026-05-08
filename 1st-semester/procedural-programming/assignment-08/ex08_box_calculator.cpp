/**
 * @file ex08_box_calculator.cpp
 * @brief Reads the three dimensions of a box and computes its surface area
 *        and volume.
 */

#include <iostream>

/** @brief Encapsulates a rectangular box with computed geometry. */
class Box {
public:
    /**
     * @brief Constructs a Box from its three dimensions.
     * @param width   Width in cm.
     * @param height  Height in cm.
     * @param depth   Depth in cm.
     */
    Box(int width, int height, int depth)
        : width_{width}, height_{height}, depth_{depth} {}

    /** @brief Returns the total surface area (2×(wh + hd + dw)). */
    [[nodiscard]] int surfaceArea() const {
        return 2 * (width_ * height_ + height_ * depth_ + depth_ * width_);
    }

    /** @brief Returns the volume (w × h × d). */
    [[nodiscard]] int volume() const {
        return width_ * height_ * depth_;
    }

private:
    int width_;
    int height_;
    int depth_;
};

int main() {
    int width{}, height{}, depth{};

    std::cout << "Enter box width  (cm): "; std::cin >> width;
    std::cout << "Enter box height (cm): "; std::cin >> height;
    std::cout << "Enter box depth  (cm): "; std::cin >> depth;

    const Box box(width, height, depth);

    std::cout << "Surface area: " << box.surfaceArea() << " cm²\n"
              << "Volume:       " << box.volume()       << " cm³\n";
    return 0;
}
