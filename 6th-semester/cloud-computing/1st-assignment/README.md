# Assignment 1 — Pcap Network Traffic Analyser

Parses a `.pcap` network capture file and produces per-protocol frequency
statistics and per-flow breakdowns for TCP and UDP traffic.

## Course
Cloud Computing — Semester 6

## Language
Python 3.10+

## How to Run

### Prerequisites
- Python 3.10+
- Install dependencies:

```bash
pip install -r requirements.txt
```

### Steps
```bash
# Analyse a capture file (output written to result.txt by default)
python main.py <path-to-pcap-file>

# Specify a custom output file
python main.py <path-to-pcap-file> -o output.txt
```

## What It Demonstrates
- Structured OOP design: `PcapParser` and `Reporter` classes with clear responsibilities
- `@dataclass` models: `Packet`, `FlowStats`, `ProtocolStats`
- `logging` module replacing all `print()` calls, with configurable formatter
- `pathlib.Path` for all file I/O
- `argparse` for robust CLI argument handling
- Type hints on every function signature
- Google-style docstrings on all public classes and methods
- Flow grouping by 4-tuple (source IP, destination IP, source port, destination port)
