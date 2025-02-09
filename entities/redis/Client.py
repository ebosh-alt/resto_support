import redis

from data.settings.setting import Config


class RedisClient:
    """Подключение к Redis и управление соединением"""

    _instance = None

    def __new__(cls, *args, **kwargs):
        config = Config()
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.connection = redis.Redis(
                host=config.redis.host,
                port=config.redis.port,
                decode_responses=True,  # Убедимся, что ответы будут строковыми
            )
        return cls._instance

    def get_connection(self):
        return self.connection
