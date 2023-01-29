import importlib
from typing import Iterable
from itertools import chain

from ..log import logger
from ..plugin import Plugin
from ..internal import Singleton


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

        yield from chain.from_iterable(self.plugins.values())
