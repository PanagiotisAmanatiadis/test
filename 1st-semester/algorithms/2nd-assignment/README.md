# DoAIGotSkills – Department of Applied Informatics Got Skills

Find the minimum number of candidates whose combined skills cover all required
competencies, using a greedy set-cover approximation algorithm.

## Course
Algorithms — Semester 1 (2018-2019)

## Language
Python 3.10+

## How to Run

### Prerequisites
- Python 3.10+

### Steps
```bash
# Run on test dataset a (Table 1 – 6 candidates, 6 skills)
python main.py TestFiles/a.txt

# Run on test dataset b (Table 2 – 7 candidates, 9 skills)
python main.py TestFiles/b.txt
```

### Expected output for `b.txt`
```
Minimum hiring selection (4 candidate(s)):
  - stathis   ['C++', 'DA', 'Java', 'PHP']
  - alexia    ['AI', 'C', 'Python']
  - kostas    ['AI', 'Java', 'Prolog']
  - petros    ['C', 'C++', 'ML']
```

## Algorithm

Greedy Set Cover:

1. Collect all required skills into a `remaining` set.
2. While `remaining` is non-empty:
   - Score each candidate by `|their_skills ∩ remaining|`.
   - Select the highest-scoring candidate.
   - Remove their skills from `remaining`.
3. Return the selected candidates.

**Complexity:** O(k × n) time, O(n + s) space,
where k = candidates selected, n = total candidates, s = number of skills.

**Approximation guarantee:** within O(log s) of the optimal solution
(set cover is NP-hard; the greedy heuristic is the best known polynomial approach).

## Input File Format

```
<skill1> <skill2> ... <skillN>
<candidate_name> <skill_a> <skill_b> ...
...
```

Line 0 lists all required skills. Each subsequent line starts with the
candidate's name followed by the skills they possess.

## What It Demonstrates
- Greedy approximation algorithm for the NP-hard set cover problem
- OOP design: `Candidate`, `CoverageResult` dataclasses + `SkillCoverageOptimizer` service
- File parsing via `pathlib.Path` with structured error handling
- Structured logging with `logging` module — no bare `print()` calls
- Type hints and Google-style docstrings throughout
