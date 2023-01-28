import asyncio
import importlib
from typing import TYPE_CHECKING, List, Dict, Iterable
from itertools import chain
from arashi.log import logger
from arashi.plugin import Plugin

if TYPE_CHECKING:
    from arashi.context import Context


_loaded_plugins: Dict[str, List[Plugin]] = {}


def load_plugin_module(name: str) -> None:
    """
    从一个 Python 模块加载插件。
    :param name: 模块名。
    """

    if name in _loaded_plugins:
        logger.warning(f"attempted to load duplicate plugin {name}")
        return

    try:
        module = importlib.import_module(name)
    except ImportError:
        logger.error(f"failed to load plugin {name}")
        return

    plugins = [p for p in module.__dict__.values() if isinstance(p, Plugin)]
    logger.success(f"loaded {len(plugins)} plugin(s) from {name}")
    _loaded_plugins[name] = plugins


def iter_plugins() -> Iterable[Plugin]:
    """
    遍历所有插件。
    :return: 用来遍历插件的迭代器。
    """

    return chain.from_iterable(_loaded_plugins.values())


async def run_plugins(ctx: "Context") -> None:
    """
    运行所有插件。
    :param ctx: 当前的 Context 对象。
    """

    await asyncio.gather(p.do_receive(ctx) for p in iter_plugins())
