"""Timer context manager for measuring execution time."""

import time
from contextlib import contextmanager
from typing import Generator, Callable


@contextmanager
def Timer() -> Generator[Callable[[], float], None, None]:
    """Context manager that yields a callable returning elapsed seconds.

    Usage:
        with Timer() as elapsed:
            do_work()
        seconds = elapsed()
    """
    start = time.perf_counter()
    yield lambda: time.perf_counter() - start
