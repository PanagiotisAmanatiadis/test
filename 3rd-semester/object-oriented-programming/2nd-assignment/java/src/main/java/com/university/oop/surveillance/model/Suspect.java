package com.university.oop.surveillance.model;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Objects;
import java.util.logging.Logger;

/**
 * Represents a surveillance suspect with phone numbers, collaborators,
 * suggested partners (friends-of-friends), and location data.
 */
public class Suspect {

    private static final Logger LOGGER = Logger.getLogger(Suspect.class.getName());

    private String name, codeName, country, city;
    private final List<String>  phoneNumbers  = new ArrayList<>();
    private final List<Suspect> collaborators = new ArrayList<>();

    public Suspect() {}

    public Suspect(String name, String codeName, String country, String city) {
        this.name = name; this.codeName = codeName;
        this.country = country; this.city = city;
    }

    public String getName()     { return name; }
    public void setName(String name) { this.name = name; }
    public String getCodeName() { return codeName; }
    public void setCodeName(String codeName) { this.codeName = codeName; }
    public String getCountry()  { return country; }
    public void setCountry(String country) { this.country = country; }
    public String getCity()     { return city; }
    public void setCity(String city) { this.city = city; }

    public List<String>  getPhoneNumbers()  { return Collections.unmodifiableList(phoneNumbers); }
    public List<Suspect> getCollaborators() { return Collections.unmodifiableList(collaborators); }
    public int getCollaboratorCount()       { return collaborators.size(); }

    public void addPhoneNumber(String number) {
        if (!phoneNumbers.contains(number)) phoneNumbers.add(number);
        else LOGGER.warning("Already registered: " + number);
    }

    public void addCollaborator(Suspect suspect) {
        if (!collaborators.contains(suspect)) collaborators.add(suspect);
    }

    public boolean isConnectedTo(Suspect suspect) { return collaborators.contains(suspect); }

    public List<Suspect> getCommonPartners(Suspect other) {
        List<Suspect> common = new ArrayList<>();
        for (Suspect s : collaborators)
            if (other.getCollaborators().contains(s)) common.add(s);
        return common;
    }

    /**
     * Returns collaborators-of-collaborators not yet directly linked (friends-of-friends).
     * Computed fresh each call.
     */
    public List<Suspect> getSuggestedPartners() {
        List<Suspect> suggestions = new ArrayList<>();
        for (Suspect c : collaborators) {
            for (Suspect fof : c.getCollaborators()) {
                if (!collaborators.contains(fof) && fof != this && !suggestions.contains(fof))
                    suggestions.add(fof);
            }
        }
        return suggestions;
    }

    public void logCollaborators() {
        for (Suspect s : collaborators) {
            String marker = country.equals(s.getCountry()) ? "*" : "";
            LOGGER.info(String.format("Name: %s | CodeName: %s%s", s.getName(), s.getCodeName(), marker));
        }
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Suspect other)) return false;
        return Objects.equals(name, other.name) && Objects.equals(codeName, other.codeName);
    }

    @Override public int hashCode() { return Objects.hash(name, codeName); }

    @Override
    public String toString() {
        return String.format("Suspect[name=%s, codeName=%s, country=%s, city=%s]",
                name, codeName, country, city);
    }
}
