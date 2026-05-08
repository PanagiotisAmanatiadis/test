package com.university.oop.containers.ui;

import com.university.oop.containers.service.Ship;

import javax.swing.*;
import java.util.logging.Logger;

/**
 * Swing frame for calculating and displaying the total shipping charge
 * and listing all containers loaded onto a {@link Ship}.
 */
public class ChargeCalculatorFrame extends JFrame {

    private static final Logger LOGGER = Logger.getLogger(ChargeCalculatorFrame.class.getName());

    private final Ship ship;

    private final JTextField resultField = new JTextField("Total charge for all containers", 28);
    private final JButton calculateButton = new JButton("Calculate Charge");
    private final JButton listButton      = new JButton("Print Containers");

    /**
     * Constructs the calculator frame.
     *
     * @param ship the ship whose containers are to be analysed
     */
    public ChargeCalculatorFrame(Ship ship) {
        this.ship = ship;

        JPanel panel = new JPanel();
        panel.add(calculateButton);
        panel.add(resultField);
        panel.add(listButton);

        calculateButton.addActionListener(e -> onCalculate());
        listButton.addActionListener(e -> onListContainers());

        setContentPane(panel);
        setTitle("Charge Calculator");
        setSize(420, 120);
        setResizable(false);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLocationRelativeTo(null);
        setVisible(true);
    }

    // ── Event handlers ────────────────────────────────────────────────────────

    private void onCalculate() {
        double total = ship.getTotalCost();
        resultField.setText(String.format("%.2f", total));
        LOGGER.info("Total shipping cost: " + total);
    }

    private void onListContainers() {
        ship.printContainers();
    }
}
