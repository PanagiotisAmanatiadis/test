package com.university.oop.surveillance.model;

import java.util.logging.Logger;

/** Represents an SMS text message communication. */
public final class Sms extends Communication {

    private static final Logger LOGGER = Logger.getLogger(Sms.class.getName());
    private final String content;

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
