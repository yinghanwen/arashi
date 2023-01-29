"""
Arashi 的 Websockets 连接
"""
import asyncio
import ujson as json


from typing import Union

from websockets.exceptions import ConnectionClosedError
from websockets.legacy.client import connect, WebSocketClientProtocol as WSClient

from arashi.config import WS_URL
from arashi.log import logger
from arashi.plugins import plugin_list


class Client:

    async def ws_client(self, ws_server: str):
        """建立 WS 链接"""
        async with connect(ws_server) as ws:
            if "meta_event_type" in json.loads(await ws.recv()):
                logger.info(f"Connected to {ws_server}")
            async for message in ws:
                self.on_message(ws, message)

    async def on_message(self, ws: WSClient, message: Union[str, bytes]):
    # https://github.com/botuniverse/onebot-11/blob/master/event/README.md
        context = json.loads(message := str(message).strip())
        if e := context.get(plugin_list):
            logger.success(f"Call returns -> {e}")
            # 响应报文通过队列传递给调用 API 的函数
        elif context.get("meta_event_type"):
            logger.success(f"Heartbeat meta event -> {context.get('self_id')}")
        else:
            logger.info(f"Received event -> {context.get('message_type')}:{context.get('post_type')}")
            await self.plugin_pool(ws, context)

    async def plugin_pool(self, ws: WSClient, context: dict):
        """遍历插件列表并匹配"""
        # todo: 修改，估计跑不起来
        for plugin in plugin_list:
            p = plugin.Plugin(context)
            if p.match():
                logger.info(f"Matched Command -> {context.get('raw_message')}")
                await p.handle()
    
    def run(self):
        while True:
            try:
                self.ws_client(WS_URL)
            except KeyboardInterrupt:
                logger.warning("Closing connection by user.")
                exit(0)
            except ConnectionClosedError:
                logger.warning("Connection closed, retrying in 5 seconds...")
                asyncio.sleep(5)
                continue
            except ConnectionRefusedError:
                logger.warning(f"{WS_URL} refused connection, retrying in 10 seconds...")
                asyncio.sleep(10)
                continue
            except Exception as e:
                logger.error(repr(e))
                logger.warning(f"Retrying in 10 seconds...")
                asyncio.sleep(10)
                continue
    