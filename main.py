import asyncio
import json
import logging
from contextlib import suppress

from data.config import dp, bot
from entities.redis.models.Task import Task
from handlers import routers
from services import middleware
from services.Bitrix.Client import ClientBitrix

logger = logging.getLogger(__name__)


def test_redis():
    s = Task.get_all_by_chat_id(-4709740170)
    print(s)
    # Создание новой задачи
    # task = Task(chat_id=12345, user_id=123456000, username="username", title="Ошибка на сайте", description="Клиент сообщил о проблеме с доступом.")
    # task.save()
    # print(f"Задача сохранена с ключом: {task.key}")
    #
    # # Добавление сообщения к задаче
    # msg = Message(text="Не могу зайти в аккаунт.")
    # task.add_message(msg)
    #
    # # Добавление вложения к задаче
    # task.add_attachment("https://example.com/file.jpg")
    #
    # # Загрузка задачи из Redis
    # loaded_task = Task.get(task.key)
    # print(loaded_task)
    # if loaded_task:
    #     print(f"Загружена задача: {loaded_task.key}")

    # Удаление задачи
    # s = loaded_task.delete()
    # print(s)


async def main() -> None:
    for router in routers:
        dp.include_router(router)
    dp.update.middleware(middleware.Logging())
    await dp.start_polling(bot)


async def test():
    data = {
        "id": "100",
        "parentId": None,
        "title": "Тестовый заголовок",
        "description": "Тестовое описание",
        "mark": None,
        "priority": "1",
        "multitask": "N",
        "notViewed": "N",
        "replicate": "N",
        "stageId": "68",
        "createdBy": "1",
        "createdDate": "2023-09-28T16:26:19+03:00",
        "responsibleId": "1",
        "changedBy": "1",
        "changedDate": "2024-04-27T18:13:50+03:00",
        "statusChangedBy": "1",
        "closedBy": "1",
        "closedDate": "2024-04-27T18:13:50+03:00",
        "activityDate": "2024-04-27T18:13:50+03:00",
        "dateStart": None,
        "deadline": None,
        "startDatePlan": None,
        "endDatePlan": None,
        "guid": "{60d47860-7a2d-491c-a424-bc52ada25bf2}",
        "xmlId": "trello_64535ae6172a2b1cfb8c8af1",
        "commentsCount": "7",
        "serviceCommentsCount": "2",
        "allowChangeDeadline": "N",
        "allowTimeTracking": "N",
        "taskControl": "N",
        "addInReport": "N",
        "forkedByTemplateId": None,
        "timeEstimate": "0",
        "timeSpentInLogs": None,
        "matchWorkTime": "N",
        "forumTopicId": "72",
        "forumId": "11",
        "siteId": "s1",
        "subordinate": "Y",
        "exchangeModified": None,
        "exchangeId": None,
        "outlookVersion": "3",
        "viewedDate": "2024-04-27T18:13:50+03:00",
        "sorting": None,
        "durationFact": None,
        "isMuted": "N",
        "isPinned": "N",
        "isPinnedInGroup": "N",
        "flowId": None,
        "descriptionInBbcode": "Y",
        "status": "5",
        "statusChangedDate": "2024-04-27T18:13:50+03:00",
        "durationPlan": None,
        "durationType": "days",
        "favorite": "N",
        "groupId": "24",
        "auditors": [],
        "accomplices": [
            "8"
        ],
        "newCommentsCount": 0,
        "group": {
            "id": "24",
            "name": "Проект ПлюшкиПодружки",
            "opened": False,
            "membersCount": 2,
            "image": "/bitrix/images/socialnetwork/workgroup/bag.png",
            "additionalData": []
        },
        "creator": {
            "id": "1",
            "name": "Максим Новиков",
            "link": "/company/personal/user/1/",
            "icon": "https://restocrm.bitrix24.ru/b26701624/resize_cache/1960/c0120a8d7c10d63c83e32398d1ec4d9e/main/3e0/3e09cee8dadb32e42f9f943807a02d92/DSCF8964.jpg.png",
            "workPosition": None
        },
        "responsible": {
            "id": "1",
            "name": "Максим Новиков",
            "link": "/company/personal/user/1/",
            "icon": "https://restocrm.bitrix24.ru/b26701624/resize_cache/1960/c0120a8d7c10d63c83e32398d1ec4d9e/main/3e0/3e09cee8dadb32e42f9f943807a02d92/DSCF8964.jpg.png",
            "workPosition": None
        },
        "accomplicesData": [],
        "auditorsData": {
            "8": {
                "id": "8",
                "name": "Александра Рыженкова",
                "link": "/company/personal/user/8/",
                "icon": "/bitrix/images/tasks/default_avatar.png",
                "workPosition": None
            }
        },
        "subStatus": "5"
    }
    file_detail = {
        "ID": 9694,
        "NAME": "D__tg_bots_resto_support_photos_AgACAgIAAxkBAAOMZ1ebpKyw7zfrqkUiusdE2_pjwI0AAivoMRtzaMBKq3YKX4vatVkBAAMCAAN4AAM2BAfile_14 (1).jpg",
        "CODE": None,
        "STORAGE_ID": "3",
        "TYPE": "file",
        "PARENT_ID": "3",
        "DELETED_TYPE": 0,
        "GLOBAL_CONTENT_VERSION": 1,
        "FILE_ID": 12376,
        "SIZE": "9042",
        "CREATE_TIME": "2024-12-16T13:45:34+03:00",
        "UPDATE_TIME": "2024-12-16T13:45:34+03:00",
        "DELETE_TIME": None,
        "CREATED_BY": "1",
        "UPDATED_BY": "1",
        "DELETED_BY": None,
        "DOWNLOAD_URL": "https://restocrm.bitrix24.ru/rest/1/2rnh22115mko3cu3/download/?token=disk%7CaWQ9OTY5NCZfPTlOcmtjSEF2SkphMlAzanJEY01wWlpGQlhQdzNET1g2%7CImRvd25sb2FkfGRpc2t8YVdROU9UWTVOQ1pmUFRsT2NtdGpTRUYyU2twaE1sQXphbkpFWTAxd1dscEdRbGhRZHpORVQxZzJ8MXwycm5oMjIxMTVta28zY3UzIg%3D%3D.nZBKtKJGrcxp68zanVpzwvCKsV4tAwQQ1aq06uaYrNA%3D",
        "DETAIL_URL": "https://restocrm.bitrix24.ru/docs/file/D__tg_bots_resto_support_photos_AgACAgIAAxkBAAOMZ1ebpKyw7zfrqkUiusdE2_pjwI0AAivoMRtzaMBKq3YKX4vatVkBAAMCAAN4AAM2BAfile_14 (1).jpg"

    }

    # task = ResponseTask(**data)
    # logger.info(task)
    # file_details = FileDetails(**data)
    # logger.info(file_details.model_dump())
    # await client.attach_file(1, [1, 2, 3, 4, 5, ])
    client = ClientBitrix()
    # file = await client.add_file(r"D:\tg_bots\resto_support\photos\AgACAgIAAxkBAAOMZ1ebpKyw7zfrqkUiusdE2_pjwI0AAivoMRtzaMBKq3YKX4vatVkBAAMCAAN4AAM2BAfile_14.jpg")
    s = await client.get_fields_task()
    logger.info(json.dumps(s, indent=4, ensure_ascii=False))
# tasks = await client.create_task(task)
# logger.info(tasks)

# logger.info(upload_file)
if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        # filename="log.logging",
        format="%(filename)s:%(lineno)d #%(levelname)-3s [%(asctime)s] - %(message)s",
        filemode="w",
        encoding="utf-8",
    )

    with suppress(KeyboardInterrupt):
        asyncio.run(main())
