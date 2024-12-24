from aiogram import Dispatcher, Bot
from environs import Env

env = Env()
env.read_env()

bot_token = env('BOT_TOKEN')
dp = Dispatcher()
bot = Bot(bot_token)
REDIS_HOST = "localhost"
REDIS_PORT = 6379
WAIT_TIME = 120  # Время ожидания дополнительных сообщений в секундах
RESPONSE_TIME = "5 минут"  # Время ожидания ответа. Встраивается в request_sent
USERNAME_BOT = "@Restocrmhelp_bot"

BASE_URL = env('BASE_URL')
