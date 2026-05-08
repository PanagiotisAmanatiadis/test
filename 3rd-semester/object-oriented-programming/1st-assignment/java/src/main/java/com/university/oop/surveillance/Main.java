package com.university.oop.surveillance;

import com.university.oop.surveillance.model.Communication;
import com.university.oop.surveillance.model.PhoneCall;
import com.university.oop.surveillance.model.Sms;
import com.university.oop.surveillance.model.Suspect;
import com.university.oop.surveillance.service.Registry;

import java.util.List;
import java.util.logging.Logger;

/**
 * Entry point for the Surveillance Registry console application.
 */
public class Main {

    private static final Logger LOGGER = Logger.getLogger(Main.class.getName());

    private Main() {}

    public static void main(String[] args) {

        // ── Suspects ──────────────────────────────────────────────────────────
        Suspect s1 = new Suspect("John Dow",   "Sleepy Dog",  "Spain", "Barcelona");
        s1.addPhoneNumber("00496955444444");
        s1.addPhoneNumber("00496955333333");

        Suspect s2 = new Suspect("Danny Rust", "Rusty Knife", "UK",    "London");
        s2.addPhoneNumber("00446999888888");

        Suspect s3 = new Suspect("Bob Robson", "Frozen Bear", "Spain", "Oslo");
        s3.addPhoneNumber("00478484777777");
        s3.addPhoneNumber("00478484666666");
        s3.addPhoneNumber("00478484222222");

        // ── Communications ────────────────────────────────────────────────────
        List<Communication> comms = List.of(
            new PhoneCall("00496955444444", "00478484777777", 15, 10, 2017, 127),
            new PhoneCall("00496955444444", "00478484777777", 16, 10, 2017, 240),
            new PhoneCall("00446999888888", "00496955333333", 17, 10, 2017,  52),
            new PhoneCall("00446999888888", "00478484777777", 18, 10, 2017, 180),
            new PhoneCall("00478484666666", "00496955333333", 19, 10, 2017, 305),
            new PhoneCall("00496955444444", "00478484222222", 20, 10, 2017, 247),
            new PhoneCall("00478484222222", "00496955333333", 21, 10, 2017,  32),
            new Sms("00496955444444", "00478484777777", 10, 10, 2017, "fancy a drink tonight?"),
            new Sms("00496955333333", "00446999888888", 11, 10, 2017, "Nitro Bomb prepared"),
            new Sms("00446999888888", "00496955444444", 12, 10, 2017, "flying to Berlin tomorrow"),
            new Sms("00478484777777", "00446999888888", 13, 10, 2017, "No internet connection today"),
            new Sms("00478484777777", "00446999888888", 14, 10, 2017, "Gun Received from Rusty Knife"),
            new Sms("00478484777777", "00446999888888", 15, 10, 2017, "Metro Attack ready"),
            new Sms("00478484666666", "00446999888888", 16, 10, 2017, "Explosives downtown have been placed")
        );

        // ── Registry setup ────────────────────────────────────────────────────
        Registry registry = new Registry();
        registry.addSuspect(s1);
        registry.addSuspect(s2);
        registry.addSuspect(s3);
        comms.forEach(registry::addCommunication);

        // ── Test 1: Suspect with most partners ────────────────────────────────
        LOGGER.info("── Test 1: Suspect with most partners ──");
        registry.getSuspectWithMostPartners().ifPresent(s ->
                LOGGER.info(s.getName() + ", " + s.getCodeName()));

        // ── Test 2: Longest phone call ────────────────────────────────────────
        LOGGER.info("── Test 2: Longest phone call ──");
        registry.getLongestPhoneCallBetween("00496955444444", "00478484777777")
                .ifPresent(PhoneCall::printInfo);

        // ── Test 3: Suspicious messages ───────────────────────────────────────
        LOGGER.info("── Test 3: Suspicious messages ──");
        List<Sms> suspicious = registry.getSuspiciousMessagesBetween("00478484777777", "00446999888888");
        suspicious.forEach(Sms::printInfo);

        // ── Test 4: Connection check ──────────────────────────────────────────
        LOGGER.info("── Test 4: Connection check ──");
        LOGGER.info("s1 connected to s3: " + s1.isConnectedTo(s3));
        LOGGER.info("s3 connected to s2: " + s3.isConnectedTo(s2));

        // ── Test 5: Common partners ───────────────────────────────────────────
        LOGGER.info("── Test 5: Common partners between s1 and s3 ──");
        s1.getCommonPartners(s3).forEach(s ->
                LOGGER.info(s.getName() + ", " + s.getCodeName()));

        // ── Test 6: Suspects from Spain ───────────────────────────────────────
        LOGGER.info("── Test 6: Suspects from Spain ──");
        registry.logSuspectsFromCountry("Spain");
    }
}
