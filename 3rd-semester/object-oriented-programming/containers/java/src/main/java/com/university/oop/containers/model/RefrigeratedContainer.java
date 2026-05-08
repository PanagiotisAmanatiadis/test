package com.university.oop.containers.model;

/**
 * A refrigerated shipping container charged based on power consumption.
 *
 * <p>Cost formula: {@code powerKw × 2000}</p>
 */
public final class RefrigeratedContainer extends Container {

    /** Cost rate per kilowatt of power. */
    private static final double RATE_PER_KW = 2000.0;

    private final double powerKw;

    /**
     * Constructs a RefrigeratedContainer.
     *
     * @param code        unique container identifier
     * @param destination destination port or city
     * @param powerKw     power consumption in kilowatts
     */
    public RefrigeratedContainer(String code, String destination, double powerKw) {
        super(code, destination);
        this.powerKw = powerKw;
    }

    /** @return power consumption in kilowatts */
    public double getPowerKw() { return powerKw; }

    @Override
    public double getCost() { return RATE_PER_KW * powerKw; }

    @Override
    public String toString() {
        return String.format("RefrigeratedContainer[code=%s, destination=%s, power=%.1f kW, cost=%.2f]",
                getCode(), getDestination(), powerKw, getCost());
    }
}
