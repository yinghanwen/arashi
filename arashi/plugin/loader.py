import asyncio
import importlib
from typing import TYPE_CHECKING, Iterable
from itertools import chain
from arashi.log import logger
from arashi.plugin import Plugin
from ..internal import Singleton

if TYPE_CHECKING:
    from arashi.context import Context


class PluginLoader(Singleton):
    def __init__(self) -> None:
        self.plugins: dict[str, list[Plugin]] = {}

    def load_module(self, name: str) -> None:
        """
        从一个 `Python` 模块加载插件。
        :param name: 模块名。
        """

        if name in self.plugins:
            logger.warning(f"attempted to load duplicate plugin {name}")
            return

        try:
            module = importlib.import_module(name)
        except ImportError:
            logger.error(f"failed to load plugin {name}")
            return

        plugins = [p for p in module.__dict__.values() if isinstance(p, Plugin)]
        logger.success(f"loaded {len(plugins)} plugin(s) from {name}")
        self.plugins[name] = plugins

    def __iter__(self) -> Iterable[Plugin]:
        """
        遍历所有插件。
        :return: 用来遍历插件的迭代器。
        """

        return chain.from_iterable(self.plugins.values())

    async def run_plugins(self, ctx: "Context") -> None:
        await asyncio.gather(p.do_receive(ctx) for p in self)
