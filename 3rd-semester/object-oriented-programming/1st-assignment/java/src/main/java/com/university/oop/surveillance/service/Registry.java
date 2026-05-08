package com.university.oop.surveillance.service;

import com.university.oop.surveillance.model.Communication;
import com.university.oop.surveillance.model.PhoneCall;
import com.university.oop.surveillance.model.Sms;
import com.university.oop.surveillance.model.Suspect;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;
import java.util.Optional;
import java.util.Set;
import java.util.logging.Logger;
import java.util.stream.Collectors;

/**
 * Central registry managing suspects and their communications.
 *
 * <p>When a communication is registered, the registry automatically derives
 * collaborator relationships between the involved suspects.</p>
 */
public class Registry {

    private static final Logger LOGGER = Logger.getLogger(Registry.class.getName());

    private static final Set<String> SUSPICIOUS_KEYWORDS =
            Set.of("Bomb", "Attack", "Gun", "Explosives");

    private final List<Suspect>       suspects       = new ArrayList<>();
    private final List<Communication> communications = new ArrayList<>();

    /** Registers a suspect in the registry. */
    public void addSuspect(Suspect suspect) {
        suspects.add(suspect);
        LOGGER.info("Registered suspect: " + suspect.getName());
    }

    /** @return unmodifiable view of all registered suspects */
    public List<Suspect> getSuspects() {
        return Collections.unmodifiableList(suspects);
    }

    /**
     * Adds a communication and automatically links involved suspects as collaborators.
     *
     * @param communication the communication to register
     */
    public void addCommunication(Communication communication) {
        communications.add(communication);

        Optional<Suspect> s1 = findSuspectByNumber(communication.getSenderNumber());
        Optional<Suspect> s2 = findSuspectByNumber(communication.getReceiverNumber());

        if (s1.isPresent() && s2.isPresent() && !s1.equals(s2)) {
            s1.get().addCollaborator(s2.get());
            s2.get().addCollaborator(s1.get());
        }
    }

    /**
     * Returns the suspect with the highest number of known collaborators.
     *
     * @return the top suspect, or empty if no suspects are registered
     */
    public Optional<Suspect> getSuspectWithMostPartners() {
        return suspects.stream()
                .max(Comparator.comparingInt(Suspect::getCollaboratorCount));
    }

    /**
     * Finds the longest phone call between two numbers (either direction).
     *
     * @param number1 first phone number
     * @param number2 second phone number
     * @return the longest PhoneCall, or empty if none found
     */
    public Optional<PhoneCall> getLongestPhoneCallBetween(String number1, String number2) {
        return communications.stream()
                .filter(c -> c.getDuration() > 0)
                .filter(c -> involves(c, number1, number2))
                .map(c -> (PhoneCall) c)
                .max(Comparator.comparingInt(PhoneCall::getDuration));
    }

    /**
     * Returns suspicious SMS messages between two numbers.
     * An SMS is suspicious if its content contains: Bomb, Attack, Gun, or Explosives.
     *
     * @param number1 first phone number
     * @param number2 second phone number
     * @return list of suspicious SMS messages
     */
    public List<Sms> getSuspiciousMessagesBetween(String number1, String number2) {
        return communications.stream()
                .filter(c -> involves(c, number1, number2))
                .filter(c -> !c.getSmsContent().isEmpty())
                .filter(c -> SUSPICIOUS_KEYWORDS.stream().anyMatch(c.getSmsContent()::contains))
                .map(c -> (Sms) c)
                .collect(Collectors.toList());
    }

    /** Logs all suspects originating from a given country. */
    public void logSuspectsFromCountry(String country) {
        suspects.stream()
                .filter(s -> s.getCountry().equals(country))
                .forEach(s -> LOGGER.info(s.getName() + " (" + s.getCodeName() + ")"));
    }

    private Optional<Suspect> findSuspectByNumber(String number) {
        return suspects.stream()
                .filter(s -> s.getPhoneNumbers().contains(number))
                .findFirst();
    }

    private boolean involves(Communication c, String num1, String num2) {
        String s = c.getSenderNumber();
        String r = c.getReceiverNumber();
        return (s.equals(num1) && r.equals(num2)) || (s.equals(num2) && r.equals(num1));
    }
}
