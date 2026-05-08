package com.university.oop.containers;

import com.university.oop.containers.model.BulkContainer;
import com.university.oop.containers.model.Container;
import com.university.oop.containers.model.RefrigeratedContainer;
import com.university.oop.containers.service.Ship;
import com.university.oop.containers.ui.ChargeCalculatorFrame;

import java.util.logging.Logger;

/**
 * Entry point for the Ship Cargo System application.
 *
 * <p>Seeds a ship with sample bulk and refrigerated containers,
 * logs the total cost, and launches the Swing charge calculator.</p>
 */
public class Main {

    private static final Logger LOGGER = Logger.getLogger(Main.class.getName());

    private Main() {}

    public static void main(String[] args) {

        Ship ship = new Ship(450);

        Container bulk1 = new BulkContainer("CYZ1011", "Madrid",    500.0);
        Container bulk2 = new BulkContainer("CYZ1012", "Barcelona", 2000.0);
        Container ref1  = new RefrigeratedContainer("CYZ1013", "Rome",   100.0);
        Container ref2  = new RefrigeratedContainer("CYZ1014", "Milano", 200.0);

        ship.addContainer(bulk1);
        ship.addContainer(bulk2);
        ship.addContainer(ref1);
        ship.addContainer(ref2);

        LOGGER.info("Total shipping cost: " + ship.getTotalCost());

        javax.swing.SwingUtilities.invokeLater(() -> new ChargeCalculatorFrame(ship));
    }
}
