# Assignment 2 — Surveillance Registry GUI (Java)

Extends Assignment 1 with a Swing desktop GUI and a
"suggested partners" (friends-of-friends) feature.

## Course
Object-Oriented Programming — Semester 3

## Language
Java 17 — Maven + Java Swing

## New Features over Assignment 1

| Feature | Description |
|---|---|
| `Suspect.getSuggestedPartners()` | Friends-of-friends not yet directly linked |
| `FindSuspectFrame` | Search suspect by name |
| `SuspectDetailFrame` | Shows identity, partners, suggested partners, co-nationals, suspicious SMS lookup |

## How to Run

### Prerequisites
- JDK 17+, Maven 3.8+

### Steps
```bash
cd 2nd-assignment/java
mvn package -q
java -jar target/surveillance-gui-1.0.0.jar
```

Type a name (e.g. `John Dow`) in the search window and click **Find**.

## What It Demonstrates
- Swing MVC: data model decoupled from UI frames
- Lambda event listeners, `SwingUtilities.invokeLater`
- `getSuggestedPartners()` — friends-of-friends graph traversal
- Streams, `Optional`, `java.util.logging`
