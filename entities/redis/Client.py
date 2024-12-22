import redis


class RedisClient:
    """Подключение к Redis и управление соединением"""

    _instance = None
    host = "localhost"
    port = 6379

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.connection = redis.Redis(
                host=cls.host,
                port=cls.port,
                decode_responses=True,  # Убедимся, что ответы будут строковыми
            )
        return cls._instance

    def get_connection(self):
        return self.connection
