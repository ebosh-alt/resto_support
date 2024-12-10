from datetime import datetime


class Message:
    """Модель сообщения"""

    def __init__(self, text: str, timestamp: str = None):
        self.text = text
        self.timestamp = timestamp or datetime.now().isoformat()

    def to_dict(self):
        """Конвертирует объект в словарь"""
        return {
            "text": self.text,
            "timestamp": self.timestamp,
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Создает объект из словаря"""
        return cls(text=data["text"], timestamp=data["timestamp"])
