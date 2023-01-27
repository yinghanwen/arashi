class Context:
    async def send(self, msg: str):
        ...

    arg: str
    message: str
    command: str
    notice: str
