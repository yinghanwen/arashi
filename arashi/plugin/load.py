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
    return chain.from_iterable(_loaded_plugins.values())


async def run_plugins(ctx: "Context") -> None:
    await asyncio.gather(p.do_receive(ctx) for p in iter_plugins())
