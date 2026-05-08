package com.university.oop.surveillance.ui;

import com.university.oop.surveillance.model.Suspect;
import com.university.oop.surveillance.service.Registry;

import javax.swing.*;
import java.util.logging.Logger;

/**
 * Swing frame that allows searching for a suspect by real name.
 * On success, opens {@link SuspectDetailFrame} for the found suspect.
 */
public class FindSuspectFrame extends JFrame {

    private static final Logger LOGGER = Logger.getLogger(FindSuspectFrame.class.getName());

    private final Registry registry;
    private final JTextField nameField  = new JTextField("Please enter suspect's name", 24);
    private final JButton    findButton = new JButton("Find");

    public FindSuspectFrame(Registry registry) {
        this.registry = registry;

        JPanel panel = new JPanel();
        panel.add(nameField);
        panel.add(findButton);
        findButton.addActionListener(e -> onFind());

        setContentPane(panel);
        setTitle("Find Suspect");
        setSize(420, 120);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLocationRelativeTo(null);
        setVisible(true);
    }

    private void onFind() {
        String query = nameField.getText().trim();
        registry.getSuspects().stream()
                .filter(s -> s.getName().equals(query))
                .findFirst()
                .ifPresentOrElse(
                        found -> { dispose(); new SuspectDetailFrame(found, registry); },
                        () -> JOptionPane.showMessageDialog(this,
                                "Suspect \"" + query + "\" not found.",
                                "Not Found", JOptionPane.WARNING_MESSAGE)
                );
    }
}
