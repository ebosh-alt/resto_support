from datetime import datetime, timedelta

import pytz
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loguru import logger

from data.config import Config, bot, COMPLETE_TASK_ID
from data.texts import statuses_texts
from entities.database import tasks
from services.Bitrix.Client import ClientBitrix
from services.keyboards import keyboards

UTC_TZ = pytz.utc
MOSCOW_TZ = pytz.timezone("Europe/Moscow")
logger = logger.bind(name="scheduler_logger")

config = Config.load()


class Scheduler:
    def __init__(self):
        self.scheduler = AsyncIOScheduler(timezone=MOSCOW_TZ)

    async def start(self):
        logger.info("🟢 Старт Scheduler...")
        self.scheduler.start()

    async def schedule_update(self):
        await self.work()

    async def work(self):
        logger.info("🔄 Обновляем список задач")
        client = ClientBitrix()
        async for task in tasks:
            if task.is_created:
                task_btx = await client.get_task(task.btx_id)
                if task.stage_id != task_btx.stageId:
                    task.stage_id = task_btx.stageId
                    job_id = f"task_{task.id}"
                    thread_id = None
                    if task.thread_id != 0:
                        thread_id = task.thread_id
                    self.scheduler.add_job(
                        self.send_message,
                        trigger="date",
                        run_date=datetime.now(MOSCOW_TZ) + timedelta(seconds=10),
                        args=[task.stage_id, task.id, task.chat_id, task.message_id, thread_id],
                        id=job_id,
                    )
                    await tasks.update(task)
                    logger.info(
                        f"📨 Создана новая задача для id={task.btx_id}"
                    )

    @staticmethod
    async def send_message(stage_id: int, task_id: int, chat_id: int, message_id: int, thread_id: int | None):
        text = statuses_texts.get(stage_id, None)
        if text is not None:
            if stage_id == COMPLETE_TASK_ID:
                kb = keyboards.complete_task
            else:
                kb = None
            await bot.send_message(chat_id=chat_id,
                                   message_thread_id=thread_id,
                                   text=text.format(task_id=task_id),
                                   reply_to_message_id=message_id,
                                   reply_markup=kb
                                   )
        else:
            logger.bind(name="scheduler_logger").warning(f"🚨 Неизвестный статус: {stage_id}")
