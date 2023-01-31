"""本模块定义了 Arashi 的各类 exception"""

class NetworkError(Exception):
    pass


class HttpRequestError(NetworkError):
    status: int
    reason: str

    def __init__(self, status: int, reason: str) -> None:
        self.status = status
        self.reason = reason

    def __repr__(self) -> str:
        return f"<HttpRequestException status={self.status} reason={self.reason}>"


class ParserException(Exception):
    pass


class ActionFailed(Exception):
    pass


class InvalidAuthentication(Exception):
    pass


class UnsupportedOperation(ActionFailed):
    pass


class InvalidOperation(ActionFailed):
    pass

class ContextError(Exception):
    pass

class UnknownError(Exception):
    """其他错误"""