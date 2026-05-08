# Containers — Ship Cargo System (Java)

A shipping cargo management system that models different container types,
calculates shipping costs per container type, and exposes a Swing GUI
for real-time cost calculation.

## Course
Object-Oriented Programming — Semester 3

## Language
Java 17 — Maven + Java Swing

## Domain Model

```
Container (abstract)
├── BulkContainer         — cost = weightKg × 10
└── RefrigeratedContainer — cost = powerKw × 2000

Ship       — capacity-bounded list of containers; total cost aggregation
ChargeCalculatorFrame — Swing GUI: calculate total / list containers
```

## Key Improvements over Original

| Issue in original | Fix applied |
|---|---|
| Class named `calculator` (lowercase, violates Java convention) | Renamed to `ChargeCalculatorFrame` following PascalCase |
| Greek field names (`kila`, `kw`) | Renamed to `weightKg`, `powerKw` |
| `System.out.println` for all output | `java.util.logging.Logger` |
| `containers.size() <= numberOfContainers` (off-by-one — allowed one extra) | Fixed to `containers.size() < capacity` |
| Inner `ButtonListener` with `if` chains | Lambda `ActionListener` per button |
| Public `ArrayList` field in `Ship` | Private, exposed via `getContainers()` returning unmodifiable list |

## How to Run

### Prerequisites
- JDK 17+
- Maven 3.8+

### Steps
```bash
cd containers/java
mvn package -q
java -jar target/ship-cargo-system-1.0.0.jar
```

## What It Demonstrates
- Abstract class hierarchy with polymorphic cost calculation
- Encapsulation with private fields and unmodifiable collections
- Stream `mapToDouble().sum()` for aggregation
- Swing GUI: lambda listeners, `SwingUtilities.invokeLater`
- Javadoc, named constants (`RATE_PER_KG`, `RATE_PER_KW`)
