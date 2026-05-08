"""Domain models for the DoAIGotSkills problem."""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Candidate:
    """A job candidate with a set of skills.

    Attributes:
        name: Full name of the candidate.
        skills: Frozenset of skill names the candidate possesses.
    """

    name: str
    skills: frozenset[str]

    def skills_matching(self, target: frozenset[str]) -> frozenset[str]:
        """Return the intersection of this candidate's skills with a target set.

        Args:
            target: The set of skills to match against.

        Returns:
            Skills that this candidate covers from the target set.
        """
        return self.skills & target


@dataclass
class CoverageResult:
    """Result of the greedy set-cover algorithm.

    Attributes:
        selected: Ordered list of candidates chosen by the algorithm.
        covered_skills: Union of all skills covered by the selected candidates.
    """

    selected: list[Candidate] = field(default_factory=list)
    covered_skills: frozenset[str] = frozenset()

    @property
    def count(self) -> int:
        """Number of candidates selected."""
        return len(self.selected)

    @property
    def names(self) -> list[str]:
        """Names of selected candidates in selection order."""
        return [c.name for c in self.selected]
