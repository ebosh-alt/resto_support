import logging

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from data.config import bot
from services.keyboards import keyboards


router = Router()
logger = logging.getLogger(__name__)


@router.callback_query(F.data == "back_start_menu")
@router.message(Command("start"))
async def start(message: Message | CallbackQuery, state: FSMContext):
    id = message.from_user.id
    await state.clear()
    await bot.send_message(
        chat_id=id,
        text="Главное меню",
        reply_markup=keyboards.start,
    )


menu_rt = router
