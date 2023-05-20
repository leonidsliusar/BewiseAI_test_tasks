class MemCache:
    __slots__ = ['__cache']

    def __init__(self):
        self.__cache: dict = {}

    def set_cache(self, collection: list[dict]):
        self.__cache['last_question'] = collection

    @property
    def get_cache(self) -> list[dict]:
        return self.__cache.get('last_question', [])

    @property
    def reset_cache(self) -> None:
        self.__cache = {}


cache = MemCache()
