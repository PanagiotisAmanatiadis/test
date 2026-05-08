package com.university.oop.surveillance.model;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Objects;
import java.util.logging.Logger;

/**
 * Represents a surveillance suspect with associated phone numbers,
 * known collaborators, and location information.
 */
public class Suspect {

    private static final Logger LOGGER = Logger.getLogger(Suspect.class.getName());

    private String name;
    private String codeName;
    private String country;
    private String city;

    private final List<String>  phoneNumbers  = new ArrayList<>();
    private final List<Suspect> collaborators = new ArrayList<>();

    public Suspect() {}

    /**
     * Constructs a Suspect with full identity information.
     *
     * @param name     real name
     * @param codeName operational alias
     * @param country  country of origin
     * @param city     city of residence
     */
    public Suspect(String name, String codeName, String country, String city) {
        this.name     = name;
        this.codeName = codeName;
        this.country  = country;
        this.city     = city;
    }

    public String getName()     { return name; }
    public void setName(String name) { this.name = name; }

    public String getCodeName() { return codeName; }
    public void setCodeName(String codeName) { this.codeName = codeName; }

    public String getCountry()  { return country; }
    public void setCountry(String country) { this.country = country; }

    public String getCity()     { return city; }
    public void setCity(String city) { this.city = city; }

    /** @return unmodifiable view of phone numbers */
    public List<String> getPhoneNumbers() {
        return Collections.unmodifiableList(phoneNumbers);
    }

    /** @return unmodifiable view of known collaborators */
    public List<Suspect> getCollaborators() {
        return Collections.unmodifiableList(collaborators);
    }

    /** @return number of known collaborators */
    public int getCollaboratorCount() { return collaborators.size(); }

    /**
     * Registers a phone number. Duplicates are silently ignored.
     *
     * @param number phone number to add
     */
    public void addPhoneNumber(String number) {
        if (!phoneNumbers.contains(number)) {
            phoneNumbers.add(number);
        } else {
            LOGGER.warning("Phone number already registered: " + number);
        }
    }

    /**
     * Adds a collaborator. Duplicates are silently ignored.
     *
     * @param suspect the collaborator to add
     */
    public void addCollaborator(Suspect suspect) {
        if (!collaborators.contains(suspect)) {
            collaborators.add(suspect);
        }
    }

    /**
     * Checks whether this suspect is directly linked to another.
     *
     * @param suspect the suspect to check
     * @return {@code true} if connected
     */
    public boolean isConnectedTo(Suspect suspect) {
        return collaborators.contains(suspect);
    }

    /**
     * Returns suspects who are collaborators of both this suspect and another.
     *
     * @param other the other suspect
     * @return list of common partners (computed fresh each call)
     */
    public List<Suspect> getCommonPartners(Suspect other) {
        List<Suspect> common = new ArrayList<>();
        for (Suspect s : collaborators) {
            if (other.getCollaborators().contains(s)) {
                common.add(s);
            }
        }
        return common;
    }

    /**
     * Logs all collaborators; marks those from the same country with {@code *}.
     */
    public void logCollaborators() {
        for (Suspect s : collaborators) {
            String marker = country.equals(s.getCountry()) ? "*" : "";
            LOGGER.info(String.format("Name: %s | CodeName: %s%s",
                    s.getName(), s.getCodeName(), marker));
        }
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Suspect other)) return false;
        return Objects.equals(name, other.name) && Objects.equals(codeName, other.codeName);
    }

    @Override
    public int hashCode() { return Objects.hash(name, codeName); }

    @Override
    public String toString() {
        return String.format("Suspect[name=%s, codeName=%s, country=%s, city=%s]",
                name, codeName, country, city);
    }
}
