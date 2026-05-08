# Best Time To Party

Find the optimal 1-hour window for a visitor to attend a charity bazaar and
meet the maximum number of celebrities, given each celebrity's half-open
attendance interval `[arrival, departure)`.

## Course
Algorithms — Semester 1 (2018-2019)

## Language
Python 3.10+

## How to Run

### Prerequisites
- Python 3.10+

### Steps
```bash
python main.py
```

Expected output (key lines):
```
Best arrival time : 20:00
Stay until        : 21:00
Celebrities found : 8
  - Metallica
  - Mötley Crüe
  - Accept
  - Black Sabbath
  - Manowar
  - Ozzy
  - Megadeth
  - Sepultura
```

## What It Demonstrates
- Algorithm design with half-open interval overlap detection
- Candidate-time reduction: only arrival times need to be evaluated as window starts
- OOP encapsulation via `Celebrity` and `AttendanceWindow` dataclasses
- Service-layer pattern (`BazaarScheduler`) separating algorithm logic from I/O
- Structured logging with `logging` module — no bare `print()` calls
- Type hints and Google-style docstrings throughout

## Assignment Deliverables
| File | Description |
|------|-------------|
| `pseudocode.md` | Algorithm in pseudocode with complexity analysis and full trace |
| `BestTime2Party.c` | Original C implementation (as required by task.pdf) |
| `src/best_time_to_party/models.py` | `Celebrity` and `AttendanceWindow` dataclasses |
| `src/best_time_to_party/services.py` | `BazaarScheduler` — core algorithm |
| `main.py` | Entry point with hardcoded schedule from task.pdf |
