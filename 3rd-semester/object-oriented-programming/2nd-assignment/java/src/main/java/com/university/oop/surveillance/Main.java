package com.university.oop.surveillance;

import com.university.oop.surveillance.model.*;
import com.university.oop.surveillance.service.Registry;
import com.university.oop.surveillance.ui.FindSuspectFrame;

import java.util.List;

/** Entry point — seeds the registry and launches the Swing GUI. */
public class Main {
    private Main() {}

    public static void main(String[] args) {
        Suspect s1 = new Suspect("John Dow",   "Sleepy Dog",  "Spain",  "Barcelona");
        s1.addPhoneNumber("00496955444444"); s1.addPhoneNumber("00496955333333");

        Suspect s2 = new Suspect("Danny Rust", "Rusty Knife", "UK",     "London");
        s2.addPhoneNumber("00446999888888");

        Suspect s3 = new Suspect("Bob Robson", "Frozen Bear", "Spain",  "Oslo");
        s3.addPhoneNumber("00478484777777"); s3.addPhoneNumber("00478484666666"); s3.addPhoneNumber("00478484222222");

        Suspect s4 = new Suspect("John Papas", "Quick Knife", "Greece", "Athens");
        s4.addPhoneNumber("0030210567888");

        List<Communication> comms = List.of(
            new PhoneCall("00496955444444", "00478484777777", 15, 10, 2019, 127),
            new PhoneCall("00496955444444", "00478484777777", 16, 10, 2019, 240),
            new PhoneCall("00446999888888", "00496955333333", 17, 10, 2019,  52),
            new PhoneCall("00446999888888", "00478484777777", 18, 10, 2019, 180),
            new PhoneCall("00478484666666", "00496955333333", 19, 10, 2019, 305),
            new PhoneCall("00496955444444", "00478484222222", 20, 10, 2019, 247),
            new PhoneCall("00478484222222", "00496955333333", 21, 10, 2019,  32),
            new Sms("00496955444444", "00478484777777", 10, 10, 2019, "fancy a drink tonight?"),
            new Sms("00496955333333", "00446999888888", 11, 10, 2019, "Nitro Bomb prepared"),
            new Sms("00446999888888", "00496955444444", 12, 10, 2019, "flying to Berlin tomorrow"),
            new Sms("00478484777777", "00446999888888", 13, 10, 2019, "No internet connection today"),
            new Sms("00478484777777", "00446999888888", 14, 10, 2019, "Gun Received from Rusty Knife"),
            new Sms("00478484777777", "00446999888888", 15, 10, 2019, "Metro Attack ready"),
            new Sms("00478484666666", "00446999888888", 16, 10, 2019, "Explosives downtown have been placed"),
            new Sms("0030210567888",  "00478484222222", 22, 10, 2019, "Meet you at Oslo")
        );

        Registry registry = new Registry();
        registry.addSuspect(s1); registry.addSuspect(s2);
        registry.addSuspect(s3); registry.addSuspect(s4);
        comms.forEach(registry::addCommunication);

        javax.swing.SwingUtilities.invokeLater(() -> new FindSuspectFrame(registry));
    }
}
