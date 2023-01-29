from typing import Any
from .log import logger


class Context:
    def __init__(self, data: dict[str, Any]):
        self.arg = ""
        self.message = ""
        self.command = ""
        self.notice = ""
        logger.debug(f"Creating context with data {data}")

    async def send(self, msg: str):
        ...
