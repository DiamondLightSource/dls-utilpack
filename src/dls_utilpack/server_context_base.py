import logging

# Utilities.
from dls_utilpack.callsign import callsign

# Base class for a Thing which has a name and traits.
from dls_utilpack.thing import Thing

logger = logging.getLogger(__name__)


class ServerContextBase(Thing):
    """
    Base class for an "async with" context which can be wrapped around a server object.

    Contains convenience methods common to all server contexts.

    The server object reference is supplied to this object externally.

    The server object must provide the follwing methods:
        - is_process_started()
        - is_process_alive()

    """

    # ----------------------------------------------------------------------------------------
    def __init__(
        self,
        thing_type,
        specification=None,
        predefined_uuid=None,
    ):
        Thing.__init__(
            self,
            thing_type,
            specification,
            predefined_uuid=predefined_uuid,
        )

        # Reference to object which is a server, such as BaseAiohttp.
        self.server = None

        # The context specification of the server's specification.
        self.context_specification = self.specification().get("context", {})

    # ----------------------------------------------------------------------------------------
    async def is_process_started(self):
        """"""

        if self.server is None:
            raise RuntimeError(f"{callsign(self)} a process has not been defined")

        try:
            return await self.server.is_process_started()
        except Exception:
            raise RuntimeError(
                f"unable to determing process started for server {callsign(self.server)}"
            )

    # ----------------------------------------------------------------------------------------
    async def is_process_alive(self):
        """"""

        if self.server is None:
            raise RuntimeError(f"{callsign(self)} a process has not been defined")

        try:
            return await self.server.is_process_alive()
        except Exception:
            raise RuntimeError(
                f"unable to determing dead or alive for server {callsign(self.server)}"
            )

    # ----------------------------------------------------------------------------------------
    async def __aenter__(self):
        """ """

        await self.aenter()

    # ----------------------------------------------------------------------------------------
    async def __aexit__(self, type, value, traceback):
        """ """

        await self.aexit(type, value, traceback)
