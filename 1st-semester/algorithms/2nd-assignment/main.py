"""Entry point – DoAIGotSkills greedy set-cover solver.

Usage:
    python main.py <input_file>

Example:
    python main.py TestFiles/b.txt
"""

import logging
import sys
from pathlib import Path

from src.do_ai_got_skills.services import InputParser, SkillCoverageOptimizer

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def main() -> None:
    """Parse input, run the optimiser, and log the hiring recommendation."""
    if len(sys.argv) != 2:
        logger.error("Usage: python main.py <input_file>")
        sys.exit(1)

    file_path = Path(sys.argv[1])

    required_skills, candidates = InputParser.parse(file_path)
    optimizer = SkillCoverageOptimizer(required_skills, candidates)
    result = optimizer.solve()

    logger.info("=" * 50)
    logger.info("Minimum hiring selection (%d candidate(s)):", result.count)
    for candidate in result.selected:
        logger.info("  - %s  %s", candidate.name, sorted(candidate.skills))
    logger.info("=" * 50)


if __name__ == "__main__":
    main()
