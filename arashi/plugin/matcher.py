import re
import asyncio
import operator
from typing import TYPE_CHECKING, Union, Callable, Awaitable


if TYPE_CHECKING:
    from arashi.context import Context


class Matcher:
    """
    Matcher 是用来匹配当前插件是否应该运行的对象，可以用 `|` 与 `&` 运算符复合使用。
    """

    def __init__(self, handler: Callable[["Context"], Awaitable[bool] | bool]):
        self._handler = handler

    def __or__(self, matcher: "Matcher") -> "Matcher":
        return self._compose(matcher, operator.or_)

    def __and__(self, matcher: "Matcher") -> "Matcher":
        return self._compose(matcher, operator.and_)

    def _compose(self, matcher: "Matcher", op: Callable[[bool, bool], bool]) -> "Matcher":
        async def handler(ctx: "Context") -> bool:
            res = await asyncio.gather(self.match(ctx), matcher.match(ctx))
            return op(*res)
        return Matcher(handler)

    async def match(self, ctx: "Context") -> bool:
        res = self._handler(ctx)
        if asyncio.iscoroutine(res):
            res = await res
        return res


def command(cmd: str) -> Matcher:
    return Matcher(lambda ctx: ctx.command == cmd)


def regex(r: Union[str, re.Pattern]) -> Matcher:
    if isinstance(r, str):
        r = re.compile(r)
    return Matcher(lambda ctx: bool(r.match(ctx.message)))


def notice(notice_type: str) -> Matcher:
    return Matcher(lambda ctx: ctx.notice == notice_type)
