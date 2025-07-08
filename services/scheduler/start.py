import asyncio
from loguru import logger
from .scheduler import Scheduler

async def start_scheduler():
    logger.bind(name="scheduler_logger").warning("🛑 Scheduler запущен.")
    scheduler = Scheduler()
    try:
        await scheduler.start()
    except Exception as e:
        logger.bind(name="scheduler_logger").exception(f"Не удалось запустить APScheduler: {e}")

    backoff = 1
    while True:
        try:
            await scheduler.schedule_update()
            backoff = 1
        except Exception as e:
            logger.bind(name="scheduler_logger").exception(f"Ошибка при обновлении задач: {e}")
            await asyncio.sleep(backoff)
            backoff = min(backoff * 2, 60)
            continue

        # если всё прошло успешно, просто ждём ровно 60 секунд
        await asyncio.sleep(60)


if __name__ == "__main__":
    try:
        asyncio.run(start_scheduler())
    except KeyboardInterrupt:
        logger.bind(name="scheduler_logger").warning("🛑 Scheduler остановлен вручную.")
