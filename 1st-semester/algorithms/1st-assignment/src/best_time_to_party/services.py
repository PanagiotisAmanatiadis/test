"""Service layer for the Best Time To Party problem."""

import logging
from collections.abc import Sequence

from .models import AttendanceWindow, Celebrity

logger = logging.getLogger(__name__)


class BazaarScheduler:
    """Determines the optimal 1-hour attendance window for a bazaar visitor.

    The algorithm evaluates every celebrity arrival time as a candidate window
    start. For each candidate `t`, it counts how many celebrities satisfy the
    overlap condition: ``arrival < t + 1  AND  departure > t``.
    The window with the highest count is returned.

    Time complexity:  O(n²) — n candidates × n celebrities each.
    Space complexity: O(n).
    """

    def __init__(self, celebrities: Sequence[Celebrity]) -> None:
        """Initialise the scheduler with the celebrity roster.

        Args:
            celebrities: Sequence of Celebrity objects with half-open
                [arrival, departure) intervals.

        Raises:
            ValueError: If the celebrity list is empty.
        """
        if not celebrities:
            raise ValueError("Celebrity list must not be empty.")
        self._celebrities = list(celebrities)
        logger.debug("BazaarScheduler initialised with %d celebrities.", len(self._celebrities))

    def find_best_window(self) -> AttendanceWindow:
        """Find the 1-hour window that maximises the number of celebrities present.

        Returns:
            An AttendanceWindow with the optimal start time and the celebrities
            present during that window.
        """
        candidate_times = {c.arrival for c in self._celebrities}
        logger.debug("Evaluating %d candidate window(s): %s", len(candidate_times), sorted(candidate_times))

        best: AttendanceWindow | None = None

        for t in sorted(candidate_times):
            present = tuple(c for c in self._celebrities if c.is_present_during(t))
            window = AttendanceWindow(start=t, celebrities_present=present)
            logger.debug("t=%02d:00 → %d celebrity/-ies present.", t, window.count)

            if best is None or window.count > best.count:
                best = window

        assert best is not None  # guaranteed because candidate_times is non-empty
        logger.info(
            "Best window: %02d:00 – %02d:00 with %d celebrity/-ies.",
            best.start,
            best.start + 1,
            best.count,
        )
        return best
