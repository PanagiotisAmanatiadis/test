package com.university.oop.containers.model;

import java.util.logging.Logger;

/**
 * Abstract base class representing a shipping container.
 *
 * <p>Each container has a unique code, a destination port, and a shipping cost
 * calculated by the concrete subclass according to its cargo type.</p>
 */
public abstract class Container {

    private static final Logger LOGGER = Logger.getLogger(Container.class.getName());

    private final String code;
    private final String destination;

    /**
     * Constructs a Container.
     *
     * @param code        unique container identifier
     * @param destination destination port or city
     */
    protected Container(String code, String destination) {
        this.code = code;
        this.destination = destination;
    }

    /** @return unique container identifier */
    public String getCode() { return code; }

    /** @return destination port or city */
    public String getDestination() { return destination; }

    /**
     * Calculates the shipping cost for this container.
     *
     * @return shipping cost in currency units
     */
    public abstract double getCost();

    /** Logs the container details. */
    public void printInfo() {
        LOGGER.info(String.format("Code: %s | Destination: %s | Cost: %.2f",
                code, destination, getCost()));
    }

    @Override
    public String toString() {
        return String.format("Container[code=%s, destination=%s, cost=%.2f]",
                code, destination, getCost());
    }
}
