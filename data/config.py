from aiogram import Dispatcher, Bot

from data.settings.setting import Config

config = Config.load()

dp = Dispatcher()
bot = Bot(config.telegram.bot_token)

WAIT_TIME = 120  # Время ожидания дополнительных сообщений в секундах
RESPONSE_TIME = "5 минут"  # Время ожидания ответа. Встраивается в request_sent
USERNAME_BOT = "@Restocrmhelp_bot"
# USERNAME_BOT = "@ooo_osbot"
