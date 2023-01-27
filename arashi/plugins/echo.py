from typing import TYPE_CHECKING
from arashi.plugin import Plugin, command

if TYPE_CHECKING:
    from arashi.context import Context


plugin = Plugin(
    name='echo',
    usage='/echo something',
    description='',
)
plugin.match(command('echo'))


@plugin.receive()
async def handle_echo_receive(ctx: "Context"):
    await ctx.send(ctx.arg)
