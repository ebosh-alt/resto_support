import logging

from aiogram import Router, F
from aiogram.types import CallbackQuery

from data.config import bot
from data.texts import complete_task_text, not_complete_task_text

router = Router()
logger = logging.getLogger(__name__)


@router.callback_query(F.data == "complete_task")
async def complete_task(message: CallbackQuery):
    id = message.message.chat.id
    await bot.edit_message_text(
        chat_id=id,
        message_id=message.message.message_id,
        text=complete_task_text,
    )


@router.callback_query(F.data == "not_complete_task")
async def not_complete_task(message: CallbackQuery):
    id = message.message.chat.id
    await bot.edit_message_text(
        chat_id=id,
        message_id=message.message.message_id,
        text=not_complete_task_text,
    )


tasks_rt = router
