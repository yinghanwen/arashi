import ujson as json
from arashi.log import logger
from asyncio.threads import to_thread

def on_message(_, message):
    # https://github.com/botuniverse/onebot-11/blob/master/event/README.md
    context = json.loads(message)
    if "echo" in context:
        logger.debug("调用返回 -> " + message)
        # 响应报文通过队列传递给调用 API 的函数
    elif "meta_event_type" in context:
        logger.debug("心跳事件 -> " + message)
    else:
        logger.info("收到事件 -> " + message)
        # 消息事件，开启线程
