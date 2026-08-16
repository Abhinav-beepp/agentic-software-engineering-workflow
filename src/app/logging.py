import json
import logging
import sys
from typing import Any


def configure_logging(level: str = "INFO") -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        stream=sys.stdout,
        format="%(message)s",
        force=True,
    )


def event(logger: logging.Logger, **fields: Any) -> None:
    logger.info(json.dumps(fields, default=str, sort_keys=True))
