import asyncio
from typing import Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from arashi.context import Context
    from .rule import Rule
    from .receiver import Receiver, ReceiverHandler


class Plugin:
    """
    `Plugin` 用来定义一个插件，通过 `receive` 装饰器来添加对应规则下的回调函数。
    """

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

    def receive(self, rule: "Rule") -> Callable[[ReceiverHandler], ReceiverHandler]:
        def wrapper(handler: "ReceiverHandler"):
            self._receivers.append(Receiver(rule, handler))
            return handler
        return wrapper

    async def do_receive(self, ctx: "Context") -> None:
        await asyncio.gather(r.receive(ctx) for r in self._receivers)
