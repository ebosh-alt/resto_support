import json
import logging
from datetime import datetime

from data.config import WAIT_TIME
from ..Client import RedisClient

logger = logging.getLogger(__name__)


class BaseModel:
    """Базовая модель для работы с Redis"""
    TTL = WAIT_TIME  # Время жизни записи в Redis (в секундах)
    REDIS_PREFIX = "model"

    def __init__(self, key: str = None):
        """Конструктор модели"""
        self.key = key

    @staticmethod
    def _generate_unique_key():
        """Генерация уникального ключа (например, по времени)"""
        return datetime.now().strftime("%Y%m%d%H%M%S%f")

    def save(self):
        """Сохраняет текущий объект в Redis"""
        connection = RedisClient().get_connection()
        data = self.to_dict()
        connection.setex(self.key, self.TTL, json.dumps(data))
        # if self.TTL:
        #     connection.expire(self.key, self.TTL)  # Устанавливаем TTL для ключа

    @classmethod
    def get(cls, key: str):
        """Загружает объект из Redis по ключу"""
        connection = RedisClient().get_connection()
        data = connection.get(key)
        if data:
            return cls.from_dict(json.loads(data))
        return None

    def delete(self):
        """Удаляет объект из Redis"""
        connection = RedisClient().get_connection()
        connection.delete(self.key)
        return True

    def to_dict(self):
        """Конвертирует объект в словарь"""
        raise NotImplementedError

    @classmethod
    def from_dict(cls, data: dict):
        """Создаёт объект из словаря"""
        raise NotImplementedError

    def _update_redis_field(self, field_name: str, value):
        """Обновляет только одно поле Redis без полной перезаписи"""
        connection = RedisClient().get_connection()
        connection.hset(self.key, field_name, json.dumps(value))
        if self.TTL:  # Устанавливаем TTL снова после обновления поля
            connection.expire(self.key, self.TTL)  # Восстанавливаем TTL
