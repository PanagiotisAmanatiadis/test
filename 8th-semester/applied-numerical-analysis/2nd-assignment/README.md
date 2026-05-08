# 3-D Distance Computation via Fast Marching Method

Implementation of the **Fast Marching Method (FMM)** for computing the Signed Distance Function
(SDF) — the distance from every point of a 3-D Cartesian grid to the nearest surface of a
geometric shape. Validated against the closed-form SDF of a sphere (R = 0.3) and an
axis-aligned cube, with mean absolute error converging at O(h) as expected.

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
# Default: 50³ grid, sphere + cube, save PNG slices to current directory
python main.py

# Higher resolution without plots (headless)
python main.py --grid-size 80 --no-plot

# Custom output directory
python main.py --output-dir results/
```

## Project Structure
```
2nd-assignment/
├── src/
│   └── fmm3d/
│       ├── grid.py        # regular 3-D Cartesian grid
│       ├── image.py       # upwind 1-D / 2-D / 3-D Eikonal solver
│       ├── shapes.py      # Sphere and Box analytic SDFs
│       ├── fmm.py         # Fast Marching Method implementation
│       └── visualizer.py  # orthogonal 2-D slice plots
├── main.py
├── requirements.txt
└── README.md
```

## What It Demonstrates

| Concept | Implementation |
|---|---|
| **Fast Marching Method** | Min-heap (priority queue) wavefront propagation seeded at the interface; `O(N³ log N)` complexity |
| **Upwind Eikonal solver** | Analytic 1-D / 2-D / 3-D quadratic solutions to `(T−a)² + (T−b)² + (T−c)² = h²`; no external numerical libraries |
| **Signed Distance Field** | Sign recovered from the analytic SDF after unsigned FMM; interior nodes receive negative distances |
| **Accuracy verification** | Mean absolute error vs. closed-form SDF reported at runtime; error scales with grid spacing `h` |
| **OOP design** | `Grid`, `Sphere`, `Box`, `FMM` as separate, fully-typed classes with Google-style docstrings |

## Algorithm Summary

1. **Interface detection** — mark nodes whose sign differs from any face-adjacent neighbour.
2. **Initialise heap** — seed interface nodes with `|analytic_sdf|` as their distance.
3. **Propagate** — repeatedly accept the node with smallest tentative distance, then update
   its six neighbours using the Eikonal stencil:

   | Available directions | Update formula |
   |---|---|
   | 1 | `T = a + h` |
   | 2 | `T = (a + b + √(2h² − (b−a)²)) / 2` |
   | 3 | `T = (a + b + c + √((a+b+c)² − 3(a²+b²+c²−h²))) / 3` |

4. **Sign recovery** — apply `sign(analytic_sdf)` to the unsigned result.
