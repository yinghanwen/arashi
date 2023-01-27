import re
from typing import TYPE_CHECKING, Union


if TYPE_CHECKING:
    from arashi.plugin.plugin import PluginMatcher
    from arashi.context import Context


def command(cmd: str) -> "PluginMatcher":
    async def matcher(ctx: "Context") -> bool:
        return ctx.command == cmd
    return matcher


def regex(r: Union[str, re.Pattern]) -> "PluginMatcher":
    if isinstance(r, str):
        r = re.compile(r)

    async def matcher(ctx: "Context") -> bool:
        return bool(r.match(ctx.message))
    return matcher


def notice(notice_type: str) -> "PluginMatcher":
    async def matcher(ctx: "Context") -> bool:
        return ctx.notice == notice_type
    return matcher
