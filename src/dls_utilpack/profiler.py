import logging
import threading
import time
from typing import Optional

logger = logging.getLogger(__name__)


class Context:
    """
    Class that holds the total execution time and call count of potentially multiple executions of the same label.
    Reports its contents as a single-line string.

    TODO: Make profiles nestable by accumulating them at the context close.
    """

    def __init__(self, label: str, profiler: Profiler):
        self.__profiler = profiler

        self.__label = label
        self.__start_time = 0

    def __enter__(self):
        self.__start_time = time.time()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__profiler.accumulate(
            self.__label,
            time.time() - self.__start_time,
        )


class Profile:
    """
    Class that holds the total execution time and call count of potentially multiple executions of the same label.
    Reports its contents as a single-line string.

    TODO: Make profiles nestable by accumulating them at the context close.
    """

    def __init__(self, label):
        self.__label = label
        self.__seconds = 0.0
        self.__count = 0

    def __str__(self):
        if self.__count == 0:
            average = 0.0
        else:
            average = self.__seconds / self.__count

        return (
            f"{self.__label} called {self.__count} times"
            f" for average of {'%0.3f' % average} seconds"
        )


class Profiler:
    """
    Class that accumulates multiple profiles.
    Reports its results as a multi-line string.
    """

    def __init__(self):
        self.__profiles = {}
        self.__lock = threading.RLock()

    def profile(self, label: str) -> Context:
        """
        Return a context to hold the profile timing.

        Args:
            label (str): label identifying the profile

        Returns:
            Profile: a new profile object, or previously existing one
        """
        return Context(label, self)

    def accumulate(self, label: str, seconds: float) -> None:
        """
        Accumulate a report into the profile for the given label.
        Uses previously existing profile, if any, or makes a new instance.

        Args:
            label (str): label identifying the profile

        Returns:
            Profile: a new profile object, or previously existing one
        """
        with self.__lock:
            profile = self.__profiles.get(label)
            if profile is None:
                profile = Profile(label)
                self.__profiles[label] = profile

        profile.seconds += seconds
        profile.count += 1

    def __str__(self) -> str:
        lines = []
        for profile in self.__profiles.values():
            lines.append(str(profile))

        return "\n".join(lines)


# A global instance for convenience.
__profiler: Optional[Profiler] = None

__global_lock = threading.RLock()


def dls_utilpack_global_profiler() -> Profiler:
    global __profiler
    global __global_lock

    with __global_lock:
        if __profiler is None:
            __profiler = Profiler()
    return __profiler
