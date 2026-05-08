"""Domain models for the Best Time To Party problem."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Celebrity:
    """A celebrity attending the charity bazaar.

    Attributes:
        name: Display name of the celebrity.
        arrival: Hour of arrival (inclusive), e.g. 20 means 20:00.
        departure: Hour of departure (exclusive), e.g. 22 means the celebrity
            leaves before 22:00 — interval is [arrival, departure).
    """

    name: str
    arrival: int
    departure: int

    def is_present_during(self, window_start: int) -> bool:
        """Return True if the celebrity overlaps the window [window_start, window_start + 1).

        Args:
            window_start: Integer hour at which the visitor arrives.

        Returns:
            True when arrival < window_start + 1 AND departure > window_start.
        """
        return self.arrival < window_start + 1 and self.departure > window_start


@dataclass(frozen=True)
class AttendanceWindow:
    """Result of evaluating a single 1-hour candidate window.

    Attributes:
        start: Integer hour at which the visitor arrives.
        celebrities_present: Tuple of celebrities present in this window.
    """

    start: int
    celebrities_present: tuple["Celebrity", ...]

    @property
    def count(self) -> int:
        """Number of celebrities present in this window."""
        return len(self.celebrities_present)
