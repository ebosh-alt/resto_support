import asyncio

from loguru import logger

from .scheduler import Scheduler

async def start_scheduler():
    logger.warning("🛑 Scheduler запущен.")
    scheduler = Scheduler()
    await scheduler.start()

    while True:
        await scheduler.schedule_update()
        await asyncio.sleep(60)


if __name__ == "__main__":
    try:
        asyncio.run(start_scheduler())
    except KeyboardInterrupt:
        logger.warning("🛑 Scheduler запущен.")
