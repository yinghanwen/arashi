import asyncio
from typing import Callable, Awaitable, overload, TYPE_CHECKING
from arashi.plugin.matcher import Matcher

if TYPE_CHECKING:
    from arashi.context import Context


PluginReceiver = Callable[["Context"], Awaitable[None]]


class Plugin:
    def __init__(self, *, on: Matcher, name: str, usage: str, description: str) -> None:
        self._name = name
        self._usage = usage
        self._description = description
        self._matcher = on
        self._receivers: list[PluginReceiver] = []

    @property
    def name(self) -> str:
        return self._name

    @property
    def usage(self) -> str:
        return self._usage

    @property
    def description(self) -> str:
        return self._description

    @overload
    def receive(self, receiver: PluginReceiver) -> None: ...

    @overload
    def receive(self) -> Callable[[PluginReceiver], PluginReceiver]: ...

    def receive(self, receiver=None):
        if receiver is not None:
            self._receivers.append(receiver)
            return

        def wrapper(f: PluginReceiver):
            self._receivers.append(f)
            return f

        return wrapper

    async def do_receive(self, ctx: "Context") -> None:
        if not await self._matcher.match(ctx):
            return
        await asyncio.gather(receiver(ctx) for receiver in self._receivers)
