# Containers — Ship Cargo System (C#)

C# port of the ship cargo management system.
Console-based: load containers onto a ship, calculate the total
shipping cost, and list all containers.

## Course
Object-Oriented Programming — Semester 3

## Language
C# 12 / .NET 8 — Console application

## Domain Model

```
Container (abstract class)
├── BulkContainer          — cost = WeightKg × 10
└── RefrigeratedContainer  — cost = PowerKw × 2000

Ship       — capacity-bounded; ILogger<Ship> injected
Program.cs — seeds ship, runs interactive console menu
```

## Console UI

```
[1] Calculate total charge
[2] List all containers
[0] Exit
```

## How to Run

### Prerequisites
- .NET 8 SDK

### Steps
```bash
cd containers/csharp
dotnet run
```

## What It Demonstrates
- Abstract class with sealed subclasses
- Named constants (`RatePerKg`, `RatePerKw`) instead of magic numbers
- `IReadOnlyList<T>` for encapsulated collections
- LINQ aggregation (`Sum`)
- `ILogger<T>` constructor injection
- XML documentation comments
- `override string ToString()` on all models
