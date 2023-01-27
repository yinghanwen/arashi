from typing import TYPE_CHECKING
from arashi.plugin import Plugin

if TYPE_CHECKING:
    from arashi.context import Context


plugin = Plugin(
    name='echo',
    usage='/echo something',
    description='',
)


@plugin.match()
async def handle_echo_match(ctx: "Context"):
    return ctx.command == 'echo'


@plugin.receive()
async def handle_echo_receive(ctx: "Context"):
    await ctx.send(ctx.arg)