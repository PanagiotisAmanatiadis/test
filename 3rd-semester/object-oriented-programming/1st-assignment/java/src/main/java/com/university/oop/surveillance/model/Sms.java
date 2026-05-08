package com.university.oop.surveillance.model;

import java.util.logging.Logger;

/**
 * Represents an SMS text message communication between two phone numbers.
 */
public final class Sms extends Communication {

    private static final Logger LOGGER = Logger.getLogger(Sms.class.getName());

    private final String content;

    /**
     * Constructs an SMS.
     *
     * @param senderNumber   the originating phone number
     * @param receiverNumber the destination phone number
     * @param day            day of the month
     * @param month          month of the year
     * @param year           four-digit year
     * @param content        the text body of the message
     */
    public Sms(String senderNumber, String receiverNumber,
               int day, int month, int year, String content) {
        super(senderNumber, receiverNumber, day, month, year);
        this.content = content;
    }

    @Override public int getDuration()      { return 0; }
    @Override public String getSmsContent() { return content; }

    @Override
    public void printInfo() {
        LOGGER.info("SMS details:");
        super.printInfo();
        LOGGER.info("Text: " + content);
    }

    @Override
    public String toString() {
        return String.format("SMS[%s, content=\"%s\"]", super.toString(), content);
    }
}
