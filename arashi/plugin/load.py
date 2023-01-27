import importlib
from typing import List, Dict, Iterable
from itertools import chain
from arashi.log import logger
from arashi.plugin import Plugin


_loaded_plugins: Dict[str, List[Plugin]] = {}


def load_plugin_module(name: str) -> None:
    if name in _loaded_plugins:
        logger.warning(f'attempted to load duplicate plugin {name}')
        return

    try:
        module = importlib.import_module(name)
    except ImportError:
        logger.error(f'failed to load plugin {name}')
        return

    logger.success(f'loaded plugin {name}')
    _loaded_plugins[name] = [p for p in module.__dict__.values() if isinstance(p, Plugin)]


# 在某个事件被触发时
# for plugin in iter_plugins():
#     await plugin.do_receive(ctx)
def iter_plugins() -> Iterable[Plugin]:
    return chain.from_iterable(_loaded_plugins.values())
