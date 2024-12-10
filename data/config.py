import redis
from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram.fsm.storage.redis import RedisStorage
from environs import Env

env = Env()
env.read_env()

bot_token = env('BOT_TOKEN')
dp = Dispatcher()
bot = Bot(bot_token)
# SQLALCHEMY_DATABASE_URL = env("SQLALCHEMY_DATABASE_URL")
ADMINS = []
REDIS_HOST = "localhost"
REDIS_PORT = 6379
WAIT_TIME = 20  # Настроить по необходимости
RESPONSE_TIME = "5 минут"  # Настроить по необходимости
USERNAME_BOT = "@ooo_osbot"
