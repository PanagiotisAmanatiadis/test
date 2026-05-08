package com.university.oop.surveillance.ui;

import com.university.oop.surveillance.model.Sms;
import com.university.oop.surveillance.model.Suspect;
import com.university.oop.surveillance.service.Registry;

import javax.swing.*;
import java.util.List;
import java.util.logging.Logger;

/**
 * Swing frame displaying detailed information about a suspect:
 * identity, phone numbers, collaborators, suggested partners,
 * co-nationals, and suspicious SMS lookup.
 */
public class SuspectDetailFrame extends JFrame {

    private static final Logger LOGGER = Logger.getLogger(SuspectDetailFrame.class.getName());

    private final Suspect  suspect;
    private final Registry registry;

    private final JTextField nameField     = new JTextField(14);
    private final JTextField codeNameField = new JTextField(14);
    private final JTextArea  numbersArea   = new JTextArea(3, 14);
    private final JTextField smsNumberField = new JTextField(14);
    private final JTextArea  smsResultArea  = new JTextArea(8, 24);
    private final JButton    findSmsButton  = new JButton("Find Suspicious SMS");
    private final JTextArea  partnersArea   = new JTextArea(8, 24);
    private final JTextArea  suggestedArea  = new JTextArea(5, 24);
    private final JTextArea  countryArea    = new JTextArea(5, 30);
    private final JButton    returnButton   = new JButton("Back to Search");

    public SuspectDetailFrame(Suspect suspect, Registry registry) {
        this.suspect  = suspect;
        this.registry = registry;

        nameField.setText(suspect.getName());
        codeNameField.setText(suspect.getCodeName());
        suspect.getPhoneNumbers().forEach(n -> numbersArea.append(n + "\n"));
        numbersArea.setEditable(false);

        suspect.getCollaborators()
                .forEach(s -> partnersArea.append(s.getName() + ", " + s.getCodeName() + "\n"));
        partnersArea.setEditable(false);

        suspect.getSuggestedPartners()
                .forEach(s -> suggestedArea.append(s.getName() + "\n"));
        suggestedArea.setEditable(false);

        countryArea.append("Suspects from " + suspect.getCountry() + "\n");
        registry.getSuspects().stream()
                .filter(s -> s.getCountry().equals(suspect.getCountry()))
                .forEach(s -> countryArea.append(s.getName() + "\n"));
        countryArea.setEditable(false);

        smsResultArea.setEditable(false);
        findSmsButton.addActionListener(e -> onFindSms());
        returnButton.addActionListener(e -> { dispose(); new FindSuspectFrame(registry); });

        JPanel main = new JPanel();
        main.setLayout(new BoxLayout(main, BoxLayout.Y_AXIS));

        JPanel row1 = new JPanel();
        row1.setBorder(BorderFactory.createTitledBorder("Identity"));
        row1.add(nameField); row1.add(codeNameField); row1.add(new JScrollPane(numbersArea));
        main.add(row1);

        JPanel row2 = new JPanel();
        row2.setBorder(BorderFactory.createTitledBorder("Suspicious SMS"));
        row2.add(smsNumberField); row2.add(findSmsButton); row2.add(new JScrollPane(smsResultArea));
        main.add(row2);

        JPanel row3 = new JPanel();
        row3.setBorder(BorderFactory.createTitledBorder("Partners"));
        row3.add(new JScrollPane(partnersArea));
        main.add(row3);

        JPanel row4 = new JPanel();
        row4.setBorder(BorderFactory.createTitledBorder("Suggested Partners"));
        row4.add(new JScrollPane(suggestedArea));
        main.add(row4);

        JPanel row5 = new JPanel();
        row5.setBorder(BorderFactory.createTitledBorder("Co-nationals"));
        row5.add(new JScrollPane(countryArea));
        main.add(row5);

        JPanel nav = new JPanel();
        nav.add(returnButton);
        main.add(nav);

        setContentPane(new JScrollPane(main));
        setTitle("Suspect — " + suspect.getName());
        setSize(560, 720);
        setResizable(false);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLocationRelativeTo(null);
        setVisible(true);
    }

    private void onFindSms() {
        smsResultArea.setText("");
        String target = smsNumberField.getText().trim();
        for (String own : suspect.getPhoneNumbers()) {
            List<Sms> results = registry.getSuspiciousMessagesBetween(own, target);
            results.forEach(sms -> smsResultArea.append(sms.getSmsContent() + "\n"));
        }
    }
}
