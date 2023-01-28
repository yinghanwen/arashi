import asyncio
from typing import Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from arashi.context import Context
    from arashi.plugin.matcher import Matcher
    from arashi.plugin.receiver import Receiver, ReceiverHandler


class Plugin:
    def __init__(self, *, name: str, usage: str, description: str) -> None:
        self._name = name
        self._usage = usage
        self._description = description
        self._receivers: list["Receiver"] = []

    @property
    def name(self) -> str:
        return self._name

    @property
    def usage(self) -> str:
        return self._usage

    @property
    def description(self) -> str:
        return self._description

    def receive(self, matcher: "Matcher") -> Callable[[ReceiverHandler], ReceiverHandler]:
        def wrapper(handler: "ReceiverHandler"):
            self._receivers.append(Receiver(matcher, handler))
            return handler
        return wrapper

    async def do_receive(self, ctx: "Context") -> None:
        await asyncio.gather(r.receive(ctx) for r in self._receivers)
