import asyncio
from typing import Callable, Awaitable, TYPE_CHECKING

if TYPE_CHECKING:
    from .rule import Rule
    from arashi.context import Context

ReceiverHandler = Callable[[Context], Awaitable[None] | None]


class Receiver:
    """
    `Receiver` 是对 `Plugin` 中的回调函数进一步包装，它只会在自己的 `rule` 通过后调用回调函数。
    """

    def __init__(self, rule: "Rule", handler: ReceiverHandler) -> None:
        self._rule = rule
        self._handler = handler

    async def receive(self, ctx: "Context") -> None:
        if not await self._rule.match(ctx):
            return

        if asyncio.iscoroutine(coro := self._handler(ctx)):
            await coro