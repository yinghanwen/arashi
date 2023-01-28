from typing import TYPE_CHECKING
from arashi.plugin import Plugin, command

if TYPE_CHECKING:
    from arashi.context import Context


plugin = Plugin(
    on=command('echo') | command('say'),
    name='echo',
    usage='/echo something or /say something',
    description='',
)


@plugin.receive()
async def handle_echo_receive(ctx: "Context"):
    await ctx.send(ctx.arg)
