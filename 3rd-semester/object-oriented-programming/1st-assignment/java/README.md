# Assignment 1 — Surveillance Registry (Java)

A surveillance system that tracks suspects and their communications
(phone calls and SMS), derives collaborator networks automatically,
and queries them for investigative insights.

## Course
Object-Oriented Programming — Semester 3

## Language
Java 17 — Maven

## Domain Model

```
Communication (abstract)
├── PhoneCall  — duration-based
└── Sms        — text content; suspicious-keyword detection

Suspect        — phone numbers, collaborators, common-partner queries
Registry       — central store; auto-links suspects via communications
```

## Key Improvements over Original

| Issue in original | Fix applied |
|---|---|
| `PhoneCall`/`Sms` redeclared all parent fields (shadowing bug — getters returned `null`) | Removed duplicate fields; all data lives in `Communication` |
| `System.out.println` throughout | `java.util.logging.Logger` |
| `Registry` accessed `protected` fields directly | All access via public getters |
| Flag-based loop in `getSuspectWithMostPartners` | Replaced with `Stream.max()` |
| `getCommonPartners` stored result in a shared field | Computed fresh each call |
| Public mutable `ArrayList` fields | `Collections.unmodifiableList` throughout |

## How to Run

### Prerequisites
- JDK 17+, Maven 3.8+

### Steps
```bash
cd 1st-assignment/java
mvn package -q
java -jar target/surveillance-registry-1.0.0.jar
```

## What It Demonstrates
- Abstract classes and polymorphism
- Encapsulation with unmodifiable collections
- `java.util.logging` structured logging
- Java Streams, `Optional<T>`, Javadoc
