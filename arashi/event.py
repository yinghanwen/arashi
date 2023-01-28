from typing import Any, List, Optional, Tuple, Union
from websockets.legacy.client import connect, WebSocketClientProtocol as WSClient
from .log import logger


async def on_message(ws: WSClient, message: Union[str, bytes]):
    # https://github.com/botuniverse/onebot-11/blob/master/event/README.md
    context = json.loads(message := str(message).strip())
    if e := context.get("echo"):
        logger.success(f"调用返回 -> {e}")
        # 响应报文通过队列传递给调用 API 的函数
        await echo.match(context)
    elif context.get("meta_event_type"):
        logger.success(f"心跳事件 -> {context.get('self_id')}")
    else:
        logger.info(f"收到事件 -> {context.get('message_type')}:{context.get('post_type')}")
        # 消息事件，检测插件
        await plugin_pool(ws, context)
