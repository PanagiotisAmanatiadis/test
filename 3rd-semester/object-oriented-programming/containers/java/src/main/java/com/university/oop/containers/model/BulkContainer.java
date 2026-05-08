package com.university.oop.containers.model;

/**
 * A shipping container carrying bulk (dry) cargo, charged at a flat rate per kilogram.
 *
 * <p>Cost formula: {@code weightKg × 10}</p>
 */
public final class BulkContainer extends Container {

    /** Cost rate per kilogram. */
    private static final double RATE_PER_KG = 10.0;

    private final double weightKg;

    /**
     * Constructs a BulkContainer.
     *
     * @param code        unique container identifier
     * @param destination destination port or city
     * @param weightKg    cargo weight in kilograms
     */
    public BulkContainer(String code, String destination, double weightKg) {
        super(code, destination);
        this.weightKg = weightKg;
    }

    /** @return cargo weight in kilograms */
    public double getWeightKg() { return weightKg; }

    @Override
    public double getCost() { return RATE_PER_KG * weightKg; }

    @Override
    public void printInfo() {
        super.printInfo();
    }

    @Override
    public String toString() {
        return String.format("BulkContainer[code=%s, destination=%s, weight=%.1f kg, cost=%.2f]",
                getCode(), getDestination(), weightKg, getCost());
    }
}
