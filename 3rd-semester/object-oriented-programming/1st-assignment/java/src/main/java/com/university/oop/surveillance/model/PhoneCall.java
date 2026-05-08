package com.university.oop.surveillance.model;

import java.util.logging.Logger;

/**
 * Represents a phone call communication between two phone numbers.
 */
public final class PhoneCall extends Communication {

    private static final Logger LOGGER = Logger.getLogger(PhoneCall.class.getName());

    private final int durationSeconds;

    /**
     * Constructs a PhoneCall.
     *
     * @param senderNumber    the originating phone number
     * @param receiverNumber  the destination phone number
     * @param day             day of the month
     * @param month           month of the year
     * @param year            four-digit year
     * @param durationSeconds call duration in seconds
     */
    public PhoneCall(String senderNumber, String receiverNumber,
                     int day, int month, int year, int durationSeconds) {
        super(senderNumber, receiverNumber, day, month, year);
        this.durationSeconds = durationSeconds;
    }

    public int getDurationSeconds() { return durationSeconds; }

    @Override public int getDuration()      { return durationSeconds; }
    @Override public String getSmsContent() { return ""; }

    @Override
    public void printInfo() {
        LOGGER.info("Phone call details:");
        super.printInfo();
        LOGGER.info("Duration: " + durationSeconds + "s");
    }

    @Override
    public String toString() {
        return String.format("PhoneCall[%s, duration=%ds]", super.toString(), durationSeconds);
    }
}
