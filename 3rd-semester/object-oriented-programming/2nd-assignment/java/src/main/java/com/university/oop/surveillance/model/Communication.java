package com.university.oop.surveillance.model;

import java.util.logging.Logger;

/** Abstract base class for a communication event between two phone numbers. */
public abstract class Communication {

    private static final Logger LOGGER = Logger.getLogger(Communication.class.getName());

    private final String senderNumber;
    private final String receiverNumber;
    private final int day, month, year;

    protected Communication(String senderNumber, String receiverNumber, int day, int month, int year) {
        this.senderNumber   = senderNumber;
        this.receiverNumber = receiverNumber;
        this.day   = day;
        this.month = month;
        this.year  = year;
    }

    public String getSenderNumber()   { return senderNumber; }
    public String getReceiverNumber() { return receiverNumber; }
    public int getDay()   { return day; }
    public int getMonth() { return month; }
    public int getYear()  { return year; }

    public void printInfo() {
        LOGGER.info(String.format("Between %s --- %s on %04d/%02d/%02d",
                senderNumber, receiverNumber, year, month, day));
    }

    public abstract int getDuration();
    public abstract String getSmsContent();

    @Override
    public String toString() {
        return String.format("%s → %s on %04d/%02d/%02d",
                senderNumber, receiverNumber, year, month, day);
    }
}
