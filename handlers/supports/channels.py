import asyncio
import logging

from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext

from data.config import bot, RESPONSE_TIME, USERNAME_BOT, WAIT_TIME
from entities.redis.models.Message import Message
from entities.redis.models.Task import Task

# Логирование
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
async def handle_message(message: types.Message, state: FSMContext):
    user_name = message.from_user.username
    user_id = message.from_user.id
    chat_id = message.chat.id
    text = message.text.replace(f"{USERNAME_BOT} ", "")
    if USERNAME_BOT in message.text:
        # task = Task.get(f"{Task.REDIS_PREFIX}:{chat_id}:{user_id}")
        task_title = " ".join(text.split()[:10])
        if Task.exists(f"{Task.REDIS_PREFIX}:{chat_id}:{user_id}"):
            await message.reply(
                f"✅ Вы уже оставили запрос недавно. Подождите немного"
            )
            return
        task = Task(
            chat_id=chat_id,
            user_id=user_id,
            username=user_name,
            title=task_title,
            message_id=message.message_id,
        )
        task.save()
        task.add_message(Message(text))

        await message.reply(
            f"✅ Ваш запрос принят"
        )
        await wait_for_followup(key=task.key, chat_id=chat_id)
    else:
        task = Task.get(f"{Task.REDIS_PREFIX}:{chat_id}:{user_id}")
        if task:
            task.add_message(Message(text))


async def wait_for_followup(key: str, chat_id: int):
    """Ожидание дополнительных сообщений и вложений в течение 2 минут"""
    await asyncio.sleep(WAIT_TIME)  # 2 минуты ожидания

    # Получаем задачу из Redis
    task = Task.get(key)
    if task:
        logger.info(task.__dict__())
        # Обновляем описание задачи новыми сообщениями
        full_description = f"Задача #{task.key}\n\n"

        for msg in task.messages:
            full_description += f"{msg.text}\n"

        # Добавляем вложения (если есть)
        if task.attachments:
            full_description += "\n**Вложения:**\n"
            for i, file_url in enumerate(task.attachments):
                full_description += f"{i + 1}. {file_url}\n"
        full_description += f"\n**Ссылка на главное сообщение:** https://t.me/c/{str(chat_id).replace("-100", "")}/{task.message_id}"
        logging.info(f"Задача обновлена:\n{full_description}")

        await bot.send_message(
            chat_id=chat_id, text=f"✅ Ваш запрос отправлен в службу поддержки, мы ответим в течение {RESPONSE_TIME}.",
            reply_to_message_id=task.message_id
        )
        task.delete()


channel_rt = router
