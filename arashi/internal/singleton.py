from typing import Optional, Any


class SingletonMeta(type):
    _singleton_instance: Optional[Any]

    def __init__(cls, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        cls._singleton_instance = None

    def __call__(cls, *args, **kwargs) -> Any:
        if not cls._singleton_instance:
            cls._singleton_instance = super().__call__(*args, **kwargs)
        return cls._singleton_instance


class Singleton(metaclass=SingletonMeta):
    __slots__ = ()
