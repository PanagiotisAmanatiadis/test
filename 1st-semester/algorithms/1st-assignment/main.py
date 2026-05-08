"""Entry point – Best Time To Party.

Loads the celebrity schedule from task.pdf (Table 1), finds the optimal
1-hour attendance window, and logs the result.
"""

import logging

from src.best_time_to_party.models import Celebrity
from src.best_time_to_party.services import BazaarScheduler

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Celebrity schedule from task.pdf, Table 1.
# Intervals are half-open: [arrival, departure).
# ---------------------------------------------------------------------------
CELEBRITIES: list[Celebrity] = [
    Celebrity("Slayer",        18, 19),
    Celebrity("Metallica",     19, 21),
    Celebrity("Scorpions",     22, 24),
    Celebrity("Mötley Crüe",   20, 22),
    Celebrity("Nazareth",      22, 23),
    Celebrity("Queensrÿche",   23, 24),
    Celebrity("Accept",        20, 22),
    Celebrity("Judas Priest",  21, 23),
    Celebrity("Black Sabbath", 19, 22),
    Celebrity("Manowar",       20, 23),
    Celebrity("Ozzy",          18, 21),
    Celebrity("Iron Maiden",   19, 20),
    Celebrity("Megadeth",      20, 21),
    Celebrity("Anthrax",       22, 24),
    Celebrity("Sepultura",     19, 23),
]


def main() -> None:
    """Run the Best Time To Party algorithm and print the result."""
    scheduler = BazaarScheduler(CELEBRITIES)
    window = scheduler.find_best_window()

    logger.info("=" * 42)
    logger.info("Best arrival time : %02d:00", window.start)
    logger.info("Stay until        : %02d:00", window.start + 1)
    logger.info("Celebrities found : %d", window.count)
    logger.info("-" * 42)
    for celebrity in window.celebrities_present:
        logger.info("  - %s", celebrity.name)
    logger.info("=" * 42)


if __name__ == "__main__":
    main()
