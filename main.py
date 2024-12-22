import asyncio
import json
import logging
from contextlib import suppress

from data.config import dp, bot
from entities.models import ResponseTask, RequestTask
from entities.redis.models.Task import Task
from handlers import routers
from services import middleware
from services.Bitrix.Client import ClientBitrix

logger = logging.getLogger(__name__)


def test_redis():
    s = Task.get_all_by_chat_id(-4709740170)
    print(s)
    # Создание новой задачи
    # task = Task(chat_id=12345, user_id=123456000, username="username", title="Ошибка на сайте", description="Клиент сообщил о проблеме с доступом.")
    # task.save()
    # print(f"Задача сохранена с ключом: {task.key}")
    #
    # # Добавление сообщения к задаче
    # msg = Message(text="Не могу зайти в аккаунт.")
    # task.add_message(msg)
    #
    # # Добавление вложения к задаче
    # task.add_attachment("https://example.com/file.jpg")
    #
    # # Загрузка задачи из Redis
    # loaded_task = Task.get(task.key)
    # print(loaded_task)
    # if loaded_task:
    #     print(f"Загружена задача: {loaded_task.key}")

    # Удаление задачи
    # s = loaded_task.delete()
    # print(s)


async def main() -> None:
    for router in routers:
        dp.include_router(router)
    dp.update.middleware(middleware.Logging())
    await dp.start_polling(bot)


async def test():
    task = RequestTask(TITLE="task.title", DESCRIPTION="task.description")
    client = ClientBitrix()
    tasks = await client.create_task(task, "test", "s")
    logger.info(tasks)

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        filename="log.logging",
        format="%(filename)s:%(lineno)d #%(levelname)-3s [%(asctime)s] - %(message)s",
        filemode="w",
        encoding="utf-8",
    )

    with suppress(KeyboardInterrupt):
        asyncio.run(main())
