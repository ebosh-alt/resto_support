import pytest
from loguru import logger
import json

from services.Bitrix.Client import ClientBitrix
from services.logger import set_logger


@pytest.fixture(scope="module")
def client():
    """Создаём реальный клиент Google Sheets."""
    return ClientBitrix()

@pytest.mark.asyncio
async def test_get_all_task(client):
    """Тест добавления строки."""
    tasks_btx = await client.get_list_task()
    for task in tasks_btx:
        logger.info(task)
    assert False

@pytest.mark.asyncio
async def test_get_task_by_id(client):
    """Тест добавления строки."""
    set_logger()
    tasks_btx = await client.get_task(18894)
    logger.info(tasks_btx.stageId)
    assert False

@pytest.mark.asyncio
async def test_get_task_fields(client):
    set_logger()
    data = await client.get_fields_task()
    logger.info(json.dumps(data, indent=4, ensure_ascii=False))
    assert False

@pytest.mark.asyncio
async def test_get_user_task_fields(client):
    set_logger()
    data = await client.get_task_user_field(796)
    logger.info(data)
    assert False