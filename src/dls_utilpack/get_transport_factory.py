import logging

import workflows.transport
from dls_utilpack.describe import describe
from dls_utilpack.explain import explain
from dls_utilpack.require import require

logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------------------
def get_transport_factory(specification):
    """"""

    thing_type = specification.get("type", "unknown-thing-type")

    transport_factory = None

    try:
        type_specific_tbd = require(
            "type_specific_tbd",
            specification,
            "type_specific_tbd",
        )
        transport_factory_specification = require(
            "type_specific_tbd",
            type_specific_tbd,
            "transport_factory",
        )

        transport_mechanism = require(
            "transport_factory_specification",
            transport_factory_specification,
            "transport_mechanism",
        )

        # Configure a transport mechanism based on the configured name.
        transport_factory = workflows.transport.lookup(transport_mechanism)

        logger.info(describe("transport_factory", transport_factory))

        if transport_mechanism == "StompTransport":
            transport_factory.config["--stomp-host"] = require(
                "transport_factory_specification",
                transport_factory_specification,
                "stomp-host",
            )
            transport_factory.config["--stomp-port"] = require(
                "transport_factory_specification",
                transport_factory_specification,
                "stomp-port",
            )
        elif transport_mechanism == "PikaTransport":
            transport_factory.config["--rabbit-host"] = require(
                "transport_factory_specification",
                transport_factory_specification,
                "rabbit-host",
            )
            transport_factory.config["--rabbit-port"] = require(
                "transport_factory_specification",
                transport_factory_specification,
                "rabbit-port",
            )
        else:
            raise RuntimeError(
                f"unrecognized transport_mechanism {transport_mechanism}"
            )

        # transport_factory.config["--stomp-user"] = "user"
        # transport_factory.config["--stomp-pass"] = "12345"
        # transport_factory.config["--stomp-prfx"] = "zocalo"
    except Exception as exception:
        raise explain(exception, f"configuring {thing_type} transport factory")

    return transport_factory
