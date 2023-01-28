import asyncio
from typing import Callable, Optional, Awaitable, overload, TYPE_CHECKING

if TYPE_CHECKING:
    from arashi.context import Context


PluginMatcher = Callable[["Context"], Awaitable[bool]]
PluginReceiver = Callable[["Context"], Awaitable[None]]


class Plugin:
    def __init__(self, *, name: str, usage: str, description: str) -> None:
        self.name = name
        self.usage = usage
        self.description = description
        self.matchers = []
        self.receivers = []

    @overload
    def match(self, matcher: PluginMatcher) -> None: ...

    @overload
    def match(self) -> Callable[[PluginMatcher], PluginMatcher]: ...

    def match(self, matcher: Optional[PluginMatcher] = None):
        if matcher:
            self.matchers.append(matcher)
            return

        def wrapper(f: PluginMatcher):
            self.matchers.append(f)
            return f

        return wrapper

    @overload
    def receive(self, receiver: PluginReceiver) -> None: ...

    @overload
    def receive(self) -> Callable[[PluginReceiver], PluginReceiver]: ...

    def receive(self, receiver: Optional[PluginReceiver] = None):
        if receiver:
            self.receivers.append(receiver)
            return

        def wrapper(f: PluginReceiver):
            self.receivers.append(f)
            return f

        return wrapper

    async def do_receive(self, ctx: "Context") -> None:
        values = await asyncio.gather(matcher(ctx) for matcher in self.matchers)
        if not all(values):
            return
        await asyncio.gather(receiver(ctx) for receiver in self.receivers)
