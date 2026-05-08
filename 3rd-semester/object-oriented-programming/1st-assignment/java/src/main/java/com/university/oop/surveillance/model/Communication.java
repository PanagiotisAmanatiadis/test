package com.university.oop.surveillance.model;

import java.util.logging.Logger;

/**
 * Abstract base class representing a communication event between two phone numbers.
 *
 * <p>A communication captures the two parties involved and the date it occurred.
 * Concrete subclasses represent specific types: {@link PhoneCall} and {@link Sms}.</p>
 */
public abstract class Communication {

    private static final Logger LOGGER = Logger.getLogger(Communication.class.getName());

    private final String senderNumber;
    private final String receiverNumber;
    private final int day;
    private final int month;
    private final int year;

    /**
     * Constructs a new Communication.
     *
     * @param senderNumber   the originating phone number
     * @param receiverNumber the destination phone number
     * @param day            day of the month (1–31)
     * @param month          month of the year (1–12)
     * @param year           four-digit year
     */
    protected Communication(String senderNumber, String receiverNumber,
                             int day, int month, int year) {
        this.senderNumber = senderNumber;
        this.receiverNumber = receiverNumber;
        this.day = day;
        this.month = month;
        this.year = year;
    }

    public String getSenderNumber()   { return senderNumber; }
    public String getReceiverNumber() { return receiverNumber; }
    public int getDay()   { return day; }
    public int getMonth() { return month; }
    public int getYear()  { return year; }

    /** Logs the communication details. */
    public void printInfo() {
        LOGGER.info(String.format("Between %s --- %s on %04d/%02d/%02d",
                senderNumber, receiverNumber, year, month, day));
    }

    /** @return call duration in seconds; {@code 0} for non-calls */
    public abstract int getDuration();

    /** @return SMS content; empty string for non-SMS communications */
    public abstract String getSmsContent();

    @Override
    public String toString() {
        return String.format("%s → %s on %04d/%02d/%02d",
                senderNumber, receiverNumber, year, month, day);
    }
}
