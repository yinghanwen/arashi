"""
Arashi 的 Websockets 连接
"""
import ujson
import asyncio

from websockets.exceptions import ConnectionClosedError
from websockets.legacy.client import connect, WebSocketClientProtocol as WSClient

from .context import Context
from .plugin import PluginLoader
from .config import WS_URL
from .log import logger


class Client:
    def __init__(self):
        self.tasks: set[asyncio.Task] = set()

    async def _listen_ws(self, ws_server: str):
        if count := len(self.tasks):
            logger.warning(f"Removing undone {count} tasks before listening.")
            self.tasks.clear()

        async with connect(ws_server) as ws:
            if "meta_event_type" in ujson.loads(await ws.recv()):
                logger.info(f"Connected to {ws_server}")
            async for message in ws:
                task = asyncio.create_task(self.handle_message(ws, message))
                self.tasks.add(task)
                task.add_done_callback(self.tasks.discard)

    async def handle_message(self, ws: WSClient, message: str | bytes):
        # https://github.com/botuniverse/onebot-11/blob/master/event/README.md
        if isinstance(message, bytes):
            message = message.decode('utf8')
        context = ujson.loads(message.strip())

        if meta_event := context.get("meta_event_type"):
            logger.success(f"Heartbeat meta event {meta_event} from {context.get('self_id')}")
            return

        logger.info(f"Received event -> {context.get('message_type')}:{context.get('post_type')}")
        await asyncio.gather(p.do_receive(Context(context)) for p in PluginLoader())

    async def listen(self):
        while True:
            try:
                await self._listen_ws(WS_URL)
            except KeyboardInterrupt:
                logger.warning("Closing connection by user")
                exit(0)
            except ConnectionClosedError:
                logger.warning("Connection closed, retrying in 5 seconds...")
                await asyncio.sleep(5)
            except ConnectionRefusedError:
                logger.warning(f"{WS_URL} refused connection, retrying in 10 seconds...")
                await asyncio.sleep(5)
            except Exception as e:
                logger.error(repr(e))
                logger.warning(f"Retrying in 10 seconds...")
                await asyncio.sleep(10)
