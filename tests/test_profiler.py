import asyncio
import logging

from dls_utilpack.profiler import dls_utilpack_global_profiler

# Base class for the tester.
from tests.base_tester import BaseTester

logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------------------
class TestProfiler(BaseTester):
    def test(self, constants, logging_setup, output_directory):
        """ """

        self.main(constants, output_directory)

    # ----------------------------------------------------------------------------------------
    async def _main_coroutine(
        self,
        constants,
        output_directory,
    ):
        """ """

        profiler = dls_utilpack_global_profiler()

        with profiler.profile("loop1"):
            await asyncio.sleep(0.1)

        logger.debug(f"profile\n{profiler}")
