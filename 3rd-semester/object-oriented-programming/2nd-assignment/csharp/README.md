# Assignment 2 — Surveillance Registry GUI (C#)

C# port of the Swing GUI assignment implemented as an interactive
console menu that mirrors all features of the original GUI screens.

## Course
Object-Oriented Programming — Semester 3

## Language
C# 12 / .NET 8 — Console application

## Console UI Flow

```
Search suspect by name → detail menu
  [1] Collaborators
  [2] Suggested partners (friends-of-friends)
  [3] Find suspicious SMS with a number
  [4] Co-nationals
  [0] Back to search
```

## How to Run

### Prerequisites
- .NET 8 SDK

### Steps
```bash
cd 2nd-assignment/csharp
dotnet run
```

## What It Demonstrates
- `GetSuggestedPartners()` — friends-of-friends graph traversal
- Interactive console UI replicating GUI screen flow
- `IReadOnlyList<T>`, nullable reference types, LINQ
- `Microsoft.Extensions.Logging` with `ILogger<T>` injection
