import asyncio
import websocket
from arashi.log import logger
from arashi.event import on_message

enable = True
url = ""
api_url = ""
event_url = ""
use_universal_client = False

class Client:
    if __name__ == '__main__':
        WS_APP = websocket.WebSocket(
            url,
            on_open=lambda _: logger.debug("连接成功......"),
            on_close=lambda _: logger.debug("重连中......"),
            on_message=on_message()
        )

        while True:
            loop = asyncio.get_event_loop()
            loop.run_forever(WS_APP)
            asyncio.sleep(5)
    