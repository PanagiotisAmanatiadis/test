package com.university.oop.surveillance.service;

import com.university.oop.surveillance.model.Communication;
import com.university.oop.surveillance.model.PhoneCall;
import com.university.oop.surveillance.model.Sms;
import com.university.oop.surveillance.model.Suspect;

import java.util.*;
import java.util.logging.Logger;
import java.util.stream.Collectors;

/** Central registry managing suspects and their communications. */
public class Registry {

    private static final Logger LOGGER = Logger.getLogger(Registry.class.getName());
    private static final Set<String> SUSPICIOUS_KEYWORDS =
            Set.of("Bomb", "Attack", "Gun", "Explosives");

    private final List<Suspect>       suspects       = new ArrayList<>();
    private final List<Communication> communications = new ArrayList<>();

    public void addSuspect(Suspect suspect) { suspects.add(suspect); }

    public List<Suspect> getSuspects() { return Collections.unmodifiableList(suspects); }

    public void addCommunication(Communication communication) {
        communications.add(communication);
        Optional<Suspect> s1 = findByNumber(communication.getSenderNumber());
        Optional<Suspect> s2 = findByNumber(communication.getReceiverNumber());
        if (s1.isPresent() && s2.isPresent() && !s1.equals(s2)) {
            s1.get().addCollaborator(s2.get());
            s2.get().addCollaborator(s1.get());
        }
    }

    public Optional<Suspect> getSuspectWithMostPartners() {
        return suspects.stream().max(Comparator.comparingInt(Suspect::getCollaboratorCount));
    }

    public Optional<PhoneCall> getLongestPhoneCallBetween(String number1, String number2) {
        return communications.stream()
                .filter(c -> c.getDuration() > 0 && involves(c, number1, number2))
                .map(c -> (PhoneCall) c)
                .max(Comparator.comparingInt(PhoneCall::getDuration));
    }

    public List<Sms> getSuspiciousMessagesBetween(String number1, String number2) {
        return communications.stream()
                .filter(c -> involves(c, number1, number2))
                .filter(c -> !c.getSmsContent().isEmpty())
                .filter(c -> SUSPICIOUS_KEYWORDS.stream().anyMatch(c.getSmsContent()::contains))
                .map(c -> (Sms) c)
                .collect(Collectors.toList());
    }

    private Optional<Suspect> findByNumber(String number) {
        return suspects.stream().filter(s -> s.getPhoneNumbers().contains(number)).findFirst();
    }

    private boolean involves(Communication c, String n1, String n2) {
        String s = c.getSenderNumber(), r = c.getReceiverNumber();
        return (s.equals(n1) && r.equals(n2)) || (s.equals(n2) && r.equals(n1));
    }
}
