import re
import asyncio
import operator
from typing import TYPE_CHECKING, Union, Callable, Awaitable


if TYPE_CHECKING:
    from arashi.context import Context


class Rule:
    """
    `Rule` 是用来检查当前插件是否应该运行的规则对象，可以用 `|` 与 `&` 运算符复合使用。
    """

    def __init__(self, handler: Callable[["Context"], Awaitable[bool] | bool]):
        self._handler = handler

    def __or__(self, rule: "Rule") -> "Rule":
        return self._compose(rule, operator.or_)

    def __and__(self, rule: "Rule") -> "Rule":
        return self._compose(rule, operator.and_)

    def _compose(self, rule: "Rule", op: Callable[[bool, bool], bool]) -> "Rule":
        async def handler(ctx: "Context") -> bool:
            res = await asyncio.gather(self.match(ctx), rule.match(ctx))
            return op(*res)
        return Rule(handler)

    async def match(self, ctx: "Context") -> bool:
        if asyncio.iscoroutine(res := self._handler(ctx)):
            res = await res
        return res


def command(cmd: str) -> Rule:
    """
    构造匹配对应命令的 `Rule` 对象。
    :param cmd: 命令内容。
    :return: 匹配命令的 `Rule` 对象。
    """

    return Rule(lambda ctx: ctx.command == cmd)


def regex(r: Union[str, re.Pattern]) -> Rule:
    """
    构造匹配对应正则的 `Rule` 对象。
    :param r: 正则表达式。
    :return: 匹配对应正则消息的 `Rule` 对象。
    """

    if isinstance(r, str):
        r = re.compile(r)
    return Rule(lambda ctx: bool(r.match(ctx.message)))


def notice(notice_type: str) -> Rule:
    """
    构造匹配对应通知的 `Rule` 对象。
    :param notice_type: 通知类型。
    :return: 匹配对应通知的 `Rule` 对象。
    """

    return Rule(lambda ctx: ctx.notice == notice_type)
