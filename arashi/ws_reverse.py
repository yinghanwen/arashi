import asyncio
import ujson as json

from websockets.exceptions import ConnectionClosedError
from websockets.legacy.client import connect

from arashi.config import WS_URL
from arashi.event import on_message
from arashi.log import logger


async def ws_client(ws_server: str):
    async with connect(ws_server) as ws:
        if "meta_event_type" in json.loads(await ws.recv()):
            logger.info(f"Connected to {ws_server}")
        async for message in ws:
            asyncio.create_task(on_message(ws, message))

class Client:
    if __name__ == '__main__':
        while True:
            try:
                asyncio.run(ws_client(WS_URL))
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
    