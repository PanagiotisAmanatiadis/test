# Anti-Missile System Simulation — Thessaloniki

Simulation of a three-site anti-missile defence network protecting the Thessaloniki
metropolitan area. An incoming missile is tracked from the moment it enters the 30 km radar
coverage zone; its full trajectory is predicted by integrating the equations of motion and
the base with the earliest intercept opportunity is selected and its launch parameters computed.

## Course
Applied Numerical Analysis — Semester 8

## Language
Python 3.10+

## How to Run

### Prerequisites
```bash
pip install -r requirements.txt
```

### Steps
```bash
# Single random missile (default seed = 42)
python main.py

# Five missiles with a custom seed
python main.py --missiles 5 --seed 123
```

## Project Structure
```
1st-assignment/
├── src/
│   └── antimissile/
│       ├── coordinates.py   # geodetic → ENU coordinate conversion
│       ├── physics.py       # missile ODE and RK4 integrator
│       ├── intercept.py     # intercept geometry and base selection
│       └── simulation.py    # main simulation loop
├── main.py
├── requirements.txt
└── README.md
```

## What It Demonstrates

| Concept | Implementation |
|---|---|
| **ODE integration (RK4)** | Missile trajectory under gravity, thrust (5 000 N), and aerodynamic drag (`Cd = 0.5`, `ρ = 1.225 kg/m³`) |
| **Intercept geometry** | Straight-line interceptor at constant speed 1 500 m/s; feasibility condition `u_a · t ≥ ‖r(t) − base‖` scanned over the discrete trajectory |
| **Base selection** | Earliest-intercept-time criterion evaluated over all three bases |
| **Coordinate conversion** | Flat-Earth geodetic (lat/lon/elev) → local ENU, accurate within the 30 km operational radius |
| **Structured logging** | All events (detection, base selection, intercept) reported in chronological order via Python `logging` |

## Physical Model

Incoming missile ODE:

```
dv/dt = g + (F_th / m) * v̂  −  (Cd · ρ · A) / (2m) · ‖v‖ · v
dr/dt = v
```

Parameters: `m = 1 000 kg`, `A = 1 m²`, `F_th = 5 000 N`, `Cd = 0.5`, `ρ = 1.225 kg/m³`,
`g = [0, 0, −9.81] m/s²`.  Time step `dt = 0.1 s`.
