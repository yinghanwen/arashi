import asyncio
from typing import Callable, Awaitable, TYPE_CHECKING
from arashi.plugin import Matcher

if TYPE_CHECKING:
    from arashi.context import Context


ReceiverHandler = Callable[[Context], Awaitable[None] | None]


class Receiver:
    def __init__(self, matcher: Matcher, handler: ReceiverHandler) -> None:
        self._matcher = matcher
        self._handler = handler

    async def receive(self, ctx: "Context") -> None:
        if not await self._matcher.match(ctx):
            return

        if asyncio.iscoroutine(coro := self._handler(ctx)):
            await coro
