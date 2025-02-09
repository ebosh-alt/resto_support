import logging

from sqlalchemy import Column, String, Integer

from .base import Base, BaseDB

logger = logging.getLogger(__name__)


class Task(Base):
    __tablename__ = "tasks"

    __allow_unmapped__ = True

    id = Column(Integer, autoincrement=True, primary_key=True)
    title = Column(String)
    description = Column(String)

    def dict(self):
        return {"id": self.id,
                "title": self.title,
                "description": self.description,
                }


class Tasks(BaseDB):
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
