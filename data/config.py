from aiogram import Dispatcher, Bot
from environs import Env

env = Env()
env.read_env()

bot_token = env('BOT_TOKEN')
dp = Dispatcher()
bot = Bot(bot_token)
REDIS_HOST = "localhost"
REDIS_PORT = 6379
WAIT_TIME = 2  # Настроить по необходимости
RESPONSE_TIME = "5 минут"  # Настроить по необходимости
USERNAME_BOT = "@ooo_osbot"

BASE_URL = env('BASE_URL')
