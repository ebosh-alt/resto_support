import asyncio
import logging

from aiogram import types, Router, F

from data import texts
from data.config import bot, USERNAME_BOT
from entities.database import tasks, Task as TaskDB
from entities.redis.models.message import Message
from entities.redis.models.tasks import Task
from services.Bitrix.Client import ClientBitrix

logger = logging.getLogger(__name__)
router = Router()


@router.message(F.photo)
async def handle_photo(message: types.Message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    task = Task.get(f"{Task.REDIS_PREFIX}:{chat_id}:{user_id}")
    if task:
        if message.caption:
            task.add_message(Message(message.caption))
        if message.photo:
            file = await bot.get_file(message.photo[-1].file_id)
            path = f"{file.file_path.split("/")[0]}/{file.file_id}{file.file_path.split("/")[1]}"
            await bot.download(file=file, destination=path)
            task.add_attachment(path)


# Функция для обработки упоминания бота
@router.message(F.text)
async def handle_message(message: types.Message):
    user_name = message.from_user.username
    user_id = message.from_user.id
    chat_id = message.chat.id
    text = message.text.replace(f"{USERNAME_BOT} ", "")
    if USERNAME_BOT in message.text:
        if Task.exists(f"{Task.REDIS_PREFIX}:{chat_id}:{user_id}"):
            await message.reply(
                texts.request_left
            )
            return
        task_title = " ".join(text.split()[:10])
        task_db = TaskDB(
            title=task_title,
            description=text,
        )
        await tasks.new(task_db)
        task_title = f"№{task_db.id:09d}. {task_title}"

        task = Task(
            chat_id=chat_id,
            db_id=task_db.id,
            chat_title=message.chat.title,
            user_id=user_id,
            username=user_name,
            title=task_title,
            description=f"{text}\n",
            message_id=message.message_id
        )
        task.save()
        task.add_message(Message(text))

        await message.reply(
            texts.request_adopted.format(task_id=task_db.id)
        )
        await wait_for_followup(key=task.key)
    else:
        task = Task.get(f"{Task.REDIS_PREFIX}:{chat_id}:{user_id}")
        if task:
            task.add_message(Message(text))
            task.description += f"{text}\n"
            task.save()


async def wait_for_followup(key: str):
    """Ожидание дополнительных сообщений и вложений в течение WAIT_TIME секунд"""
    await asyncio.sleep(10)  # ожидание

    # Получаем задачу из Redis
    task = Task.get(key)
    if task:
        task_title = f"№{task.db_id:09d}. {" ".join(task.description.split()[:10])}"
        task.title = task_title
        task.description += f"\nСсылка на главное сообщение: https://t.me/c/{str(task.chat_id).replace("-100", "")}/{task.message_id}"
        task.save()
        # await bot.send_message(chat_id=task.chat_id,
        #                        text=texts.request_sent,
        #                        reply_to_message_id=task.message_id)
        client = ClientBitrix()
        task_btx = await client.create_task(task,
                                            link=f"https://t.me/c/{str(task.chat_id).replace("-100", "")}/{task.message_id}",
                                            chat_title=task.chat_title)
        logger.info(f"Task send {task.title}")
        if task_btx:
            if task.attachments:
                files_detail = await client.add_files(task.attachments)
                logger.info(files_detail)
                ids_files = []
                for file_detail in files_detail:
                    ids_files.append(file_detail.ID)
                await client.attach_files(task_btx.id, ids_files)
        task.delete()


channel_rt = router
