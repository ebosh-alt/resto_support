import asyncio
from loguru import logger
from contextlib import suppress
from data.config import dp, bot
from entities.database.base import create_async_database
from handlers import routers
from services import middleware
from services.logger import set_logger
from services.scheduler.start import start_scheduler


@logger.catch()
async def main() -> None:
    await create_async_database()
    set_logger()
    for router in routers:
        dp.include_router(router)
    dp.update.middleware(middleware.Logging())
    asyncio.create_task(start_scheduler())  # noqa
    await bot.delete_webhook()
    await dp.start_polling(bot)


if __name__ == "__main__":
    with suppress(KeyboardInterrupt):
        asyncio.run(main()) # noqa

