"""Service layer – greedy set-cover solver and input parser."""

import logging
from pathlib import Path

from .models import Candidate, CoverageResult

logger = logging.getLogger(__name__)


class InputParser:
    """Parses a skill-coverage input file into structured domain objects.

    File format (whitespace-delimited):
        Line 0 : space-separated list of required skills
        Line 1+: <candidate_name> <skill1> <skill2> ...
    """

    @staticmethod
    def parse(file_path: Path) -> tuple[frozenset[str], list[Candidate]]:
        """Read and parse the input file.

        Args:
            file_path: Path to the input text file.

        Returns:
            A tuple of (required_skills, candidates).

        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If the file contains fewer than two lines.
        """
        if not file_path.exists():
            raise FileNotFoundError(f"Input file not found: {file_path}")

        lines = [
            line.strip().split()
            for line in file_path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]

        if len(lines) < 2:
            raise ValueError(f"Input file must have at least 2 lines, got {len(lines)}.")

        required_skills: frozenset[str] = frozenset(lines[0])
        candidates: list[Candidate] = [
            Candidate(name=row[0], skills=frozenset(row[1:]))
            for row in lines[1:]
        ]

        logger.debug(
            "Parsed %d required skill(s) and %d candidate(s) from '%s'.",
            len(required_skills),
            len(candidates),
            file_path.name,
        )
        return required_skills, candidates


class SkillCoverageOptimizer:
    """Finds the minimum-size subset of candidates that covers all required skills.

    Uses a greedy set-cover heuristic: at each iteration, select the candidate
    whose skills overlap most with the remaining uncovered skills.

    This is an approximation algorithm. Set cover is NP-hard, but the greedy
    approach guarantees a solution within O(log n) of the optimal, where n is
    the number of required skills.

    Time complexity:  O(k * n) where k = candidates selected, n = total candidates.
    Space complexity: O(n + s) where s = number of skills.
    """

    def __init__(self, required_skills: frozenset[str], candidates: list[Candidate]) -> None:
        """Initialise the optimiser.

        Args:
            required_skills: The full set of skills that must be covered.
            candidates: All available candidates with their skill sets.

        Raises:
            ValueError: If required_skills or candidates is empty.
        """
        if not required_skills:
            raise ValueError("Required skills must not be empty.")
        if not candidates:
            raise ValueError("Candidate list must not be empty.")

        self._required_skills = required_skills
        self._candidates = candidates
        logger.debug(
            "SkillCoverageOptimizer initialised: %d skill(s), %d candidate(s).",
            len(required_skills),
            len(candidates),
        )

    def solve(self) -> CoverageResult:
        """Run the greedy set-cover algorithm.

        At each step:
          1. Score every remaining candidate by how many uncovered skills they possess.
          2. Select the highest-scoring candidate (ties broken by list order).
          3. Mark their skills as covered and remove them from the pool.
          4. Repeat until all required skills are covered.

        Returns:
            A CoverageResult containing the selected candidates in order of selection.
        """
        result = CoverageResult()
        remaining_skills: frozenset[str] = self._required_skills
        pool: list[Candidate] = list(self._candidates)

        logger.info("Starting greedy set-cover. Required skills: %s", sorted(remaining_skills))

        while remaining_skills:
            best = max(pool, key=lambda c: len(c.skills_matching(remaining_skills)))
            matched = best.skills_matching(remaining_skills)

            logger.debug(
                "Selected '%s' covering %d new skill(s): %s.",
                best.name,
                len(matched),
                sorted(matched),
            )

            result.selected.append(best)
            result.covered_skills = result.covered_skills | best.skills
            remaining_skills = remaining_skills - best.skills
            pool.remove(best)

        logger.info(
            "Done. %d candidate(s) selected: %s.",
            result.count,
            result.names,
        )
        return result
