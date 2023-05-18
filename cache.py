class MemCache:
    __slots__ = ['cache']

    def __init__(self):
        self.cache: dict = {}

    def set_cache(self, collection: list[dict]):
        self.cache['last_question'] = collection

    @property
    def get_cache(self) -> list[dict]:
        return self.cache.get('last_question', [])


cache = MemCache()
