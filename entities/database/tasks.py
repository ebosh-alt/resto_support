import logging

from sqlalchemy import Column, String, Integer, Boolean, BigInteger

from .base import Base, BaseDB

logger = logging.getLogger(__name__)


class Task(Base):
    __tablename__ = "tasks"
    __allow_unmapped__ = True

    id = Column(Integer, autoincrement=True, primary_key=True)
    title = Column(String)
    description = Column(String)
    chat_id = Column(BigInteger)
    thread_id = Column(BigInteger)
    btx_id = Column(BigInteger, default=0)
    stage_id = Column(BigInteger, default=0)
    message_id = Column(BigInteger, default=0)
    is_created = Column(Boolean, default=False)

    refs = []

    def dict(self):
        return {"id": self.id,
                "title": self.title,
                "description": self.description,
                "chat_id": self.chat_id,
                "thread_id": self.thread_id,
                "btx_id": self.btx_id,
                "stage_id": self.stage_id,
                "message_id": self.message_id,
                "is_created": self.is_created,
                }


class Tasks(BaseDB[Task]):
    def __init__(self):
        super().__init__(Task)

    async def new(self, task: Task):
        await self._add_obj(task)

    async def get(self, id: int) -> Task | None:
        result = await self._get_object(id)
        return result

    async def update(self, task: Task) -> None:
        await self._update_obj(instance=task)

    async def delete(self, task: Task) -> None:
        await self._delete_obj(instance=task)

    async def in_(self, id: int) -> Task | bool:
        result = await self.get(id)
        if type(result) is Task:
            return result
        return False
