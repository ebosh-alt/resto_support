import json
import logging
from datetime import datetime

from entities.redis.Client import RedisClient
from entities.redis.models.Base import BaseModel
from entities.redis.models.Message import Message

logger = logging.getLogger(__name__)


class Task(BaseModel):
    """Модель задачи"""

    REDIS_PREFIX = "task"

    def __init__(self, chat_id: int, chat_title: str, user_id: int, username: str, title: str, description: str, message_id: int,
                 key: str = None):
        self.chat_id = chat_id
        self.chat_title = chat_title
        self.user_id = user_id
        self.username = username
        self.title = title
        self.description = description
        self.message_id = message_id
        self.messages = []
        self.attachments = []
        self.created_at = datetime.now().isoformat()
        super().__init__(key or f"{self.REDIS_PREFIX}:{chat_id}:{user_id}")

    def to_dict(self):
        """Конвертирует объект в словарь для Redis"""
        return {
            "chat_id": self.chat_id,
            "chat_title": self.chat_title,
            "user_id": self.user_id,
            "username": self.username,
            "title": self.title,
            "description": self.description,
            "message_id": self.message_id,
            "messages": json.dumps([Message.to_dict(i) for i in self.messages]),
            "attachments": json.dumps(self.attachments),
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Создаёт объект из словаря"""
        task = cls(
            user_id=int(data["user_id"]),
            chat_title=data["chat_title"],
            chat_id=int(data["chat_id"]),
            username=data["username"],
            title=data["title"],
            description=data["description"],
            message_id=data["message_id"],
            key=data.get("key"),
        )

        task.messages = data.get("messages", [])
        if task.messages:
            task.messages = [Message.from_dict(i) for i in task.messages]
        task.attachments = data.get("attachments", [])
        task.created_at = data.get("created_at")
        return task

    def __dict__(self):
        return {
            "key": self.key,
            "chat_id": self.chat_id,
            "chat_title": self.chat_title,
            "user_id": self.user_id,
            "username": self.username,
            "title": self.title,
            "description": self.description,
            "message_id": self.message_id,
            "messages": self.messages,
            "attachments": self.attachments,
            "created_at": self.created_at,
        }

    @classmethod
    def get(cls, key: str):
        """Получает задачу по ключу"""
        connection = RedisClient().get_connection()
        data = connection.hgetall(key)
        if data:
            data['messages'] = json.loads(data['messages']) if 'messages' in data else []
            data['attachments'] = json.loads(data['attachments']) if 'attachments' in data else []
            # logger.info(json.dumps(cls.from_dict(data).__dict__(), indent=4, ensure_ascii=False))
            return cls.from_dict(data)
        return None

    def save(self):
        """Сохраняет текущий объект в Redis"""
        connection = RedisClient().get_connection()
        data = self.to_dict()
        connection.hset(self.key, mapping=data)

    def delete(self):
        """Удаляет текущую задачу из Redis"""
        connection = RedisClient().get_connection()
        connection.delete(self.key)
        return True

    @classmethod
    def exists(cls, key):
        """Проверяет, существует ли ключ задачи в Redis"""
        connection = RedisClient().get_connection()
        exists = connection.exists(key)  # EXISTS возвращает 1 или 0
        return exists == 1

    @classmethod
    def get_all_by_chat_id(cls, chat_id: int):
        """Возвращает все задачи по chat_id"""
        connection = RedisClient().get_connection()
        keys = connection.keys(f"{cls.REDIS_PREFIX}:{chat_id}:*")
        tasks = []
        for key in keys:
            task = cls.get(key)
            if task:
                tasks.append(task)
        return tasks

    def add_attachment(self, file_url: str):
        """Добавляет вложение (ссылку) в задачу"""
        updated_task = self.get(self.key)
        if updated_task:
            self.attachments = updated_task.attachments
        if not isinstance(self.attachments, list):
            self.attachments = []
        self.attachments.append(file_url)
        self._update_redis_field('attachments', self.attachments)

    def add_message(self, message):
        """Добавляет сообщение в задачу"""
        updated_task = self.get(self.key)
        self.messages.append(message)
        messages = []
        if updated_task:
            messages = [Message.to_dict(i) for i in updated_task.messages]
        messages.append(message.to_dict())
        self._update_redis_field('messages', messages)
