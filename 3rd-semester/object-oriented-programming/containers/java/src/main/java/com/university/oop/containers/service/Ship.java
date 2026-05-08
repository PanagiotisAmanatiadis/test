package com.university.oop.containers.service;

import com.university.oop.containers.model.Container;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.logging.Logger;

/**
 * Represents a cargo ship with a fixed maximum container capacity.
 *
 * <p>Manages a fleet of {@link Container} objects, computes the total
 * shipping cost, and supports listing all loaded containers.</p>
 */
public class Ship {

    private static final Logger LOGGER = Logger.getLogger(Ship.class.getName());

    private final int capacity;
    private final List<Container> containers = new ArrayList<>();

    /**
     * Constructs a Ship.
     *
     * @param capacity maximum number of containers this ship can carry
     */
    public Ship(int capacity) {
        this.capacity = capacity;
    }

    /** @return maximum container capacity */
    public int getCapacity() { return capacity; }

    /** @return unmodifiable view of all loaded containers */
    public List<Container> getContainers() {
        return Collections.unmodifiableList(containers);
    }

    /**
     * Loads a container onto the ship if capacity allows.
     *
     * @param container the container to load
     */
    public void addContainer(Container container) {
        if (containers.size() < capacity) {
            containers.add(container);
        } else {
            LOGGER.warning("Ship at full capacity (" + capacity + "). Cannot add: " + container.getCode());
        }
    }

    /**
     * Calculates the total shipping cost for all loaded containers.
     *
     * @return total cost
     */
    public double getTotalCost() {
        return containers.stream()
                .mapToDouble(Container::getCost)
                .sum();
    }

    /** Logs the details of all loaded containers. */
    public void printContainers() {
        containers.forEach(Container::printInfo);
    }
}
