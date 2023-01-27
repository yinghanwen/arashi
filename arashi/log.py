"""
本模块是 arashi 的日志库，使用 loguru 记录日志信息。
"""

import sys
import loguru
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # avoid sphinx autodoc resolve annotation failed
    # because loguru module do not have `Logger` class actually
    from loguru import Logger, Record




logger: "Logger" = loguru.logger
"""
Arashi 日志记录器对象
默认信息:
- 格式: `[arashi] %(asctime)s - %(levelname)s - %(message)s`
- 等级: `INFO` ，根据 `config.log_level` 配置改变
- 输出: 输出至 stdout
用法:
    ```python
    from arashi.log import logger
    ```
"""




def default_filter(record: "Record"):
    """默认的日志过滤器，根据 `config.log_level` 配置改变日志等级。"""
    log_level = record["extra"].get("arashi_log_level", "INFO")
    levelno = logger.level(log_level).no if isinstance(log_level, str) else log_level
    return record["level"].no >= levelno


log_format: str = (
    "<g>[arashi]</g> %(asctime)s - %(levelname)s - %(message)s"
)


logger.remove()
logger_id = logger.add(
    sys.stdout,
    level=0,
    diagnose=False,
    filter=default_filter,
    format=log_format,
)

logger.add('runtime_{time}.log', rotation='50 MB', retention='3 days', encoding='utf-8')