from typing import TYPE_CHECKING
from ..plugin import Plugin, command

if TYPE_CHECKING:
    from ..context import Context


plugin = Plugin(
    name='echo',
    usage='/echo something or /say something',
    description='',
)


@plugin.receive(command('echo') | command('say'))
async def handle_echo_receive(ctx: "Context"):
    await ctx.send(ctx.arg)
