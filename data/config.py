from typing import Dict

from aiogram import Dispatcher, Bot

from data.settings.setting import Config

config = Config.load()

dp = Dispatcher()
bot = Bot(config.telegram.bot_token)

WAIT_TIME = 10  # Время ожидания дополнительных сообщений в секундах
RESPONSE_TIME = "5 минут"  # Время ожидания ответа. Встраивается в request_sent
# USERNAME_BOT = "@Restocrmhelp_bot"
USERNAME_BOT = "@design_skill_bot"

STATUSES_TASK: Dict[int, str] = {
    796: "новые задачи",
    1008: "Критические, срочные",
    798: "В работе",
    918: "Уточняем детали у клиента",
    906: "у поддержки вендора",
    1080: "Уточняем инфо для решения",
    908: "передано разработчикам",
    810: "На тестировании у клиента",
    800: "Готово",
    806: "Отложено",
    808: "3-я линия",
}

COMPLETE_TASK_ID = 800
WORK_TASK_ID = 798
