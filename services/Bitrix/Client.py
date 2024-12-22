import base64
import json
import logging
from datetime import datetime
from xml.etree.ElementTree import indent

from entities.models import ResponseTask, ApiPoint, RequestTask, UploadFile, FileDetails
from entities.redis.models.Task import Task
from services.Bitrix.Base import BaseClient

logger = logging.getLogger(__name__)


class ClientBitrix(BaseClient):
    def __init__(self):
        super().__init__()

    async def get_fields_task(self):
        response = self._get(ApiPoint.taskGetFields)
        if response.get("status") == "success":
            return True
        return response["result"]["fields"]

    async def get_list_task(self) -> list[ResponseTask] | bool:
        response = self._get(ApiPoint.listTask)
        if response.get("error"):
            return False
        list_task = []
        for task in response["result"]["tasks"]:
            list_task.append(ResponseTask(**task))
        return list_task

    async def create_task(self, task: Task | RequestTask, link: str, chat_title: str) -> ResponseTask | bool:
        if type(task) is Task:
            task = RequestTask(TITLE=task.title, DESCRIPTION=task.description)
        task.UF_AUTO_370133723970 = link
        task.UF_AUTO_159915603538 = datetime.now()
        task.UF_AUTO_474459663205 = chat_title

        params = {
            'fields': task.model_dump()
        }
        logger.info(task)
        response = self._get(ApiPoint.createTask, params=params)
        logger.info(json.dumps(response, indent=4, ensure_ascii=False))
        if response.get("error"):
            return False
        return ResponseTask(**response["result"]["task"])

    async def add_file(self, file_path: str) -> FileDetails | bool:
        with open(file_path, 'rb') as file:
            file_bytes = file.read()  # Считываем файл в байтах
            file_base64 = base64.b64encode(file_bytes)

        data = {"data": {"NAME": file_path},
                "fileContent": file_base64}
        upload_file = UploadFile(**data)
        params = upload_file.model_dump()

        response = await self._post(ApiPoint.addFile, params=params)
        if response.get("error"):
            return False
        return FileDetails(**response["result"])

    async def attach_files(self, id_task: int, id_files: list):
        params = {"taskId": id_task}
        result = []
        for id_file in id_files:
            params.update({"fileId": id_file})
            response = self._get(ApiPoint.filesAttach, params=params)
            result.append(response)
        return result

    async def add_files(self, file_paths: list) -> list[FileDetails]:
        files_detail = []
        for file_path in file_paths:
            file_detail = await self.add_file(file_path)
            files_detail.append(file_detail)
        return files_detail

    async def storage_get_list(self):
        response = self._get(ApiPoint.storageGetlist)
        if response.get("status") == "success":
            return True
        return response

    async def get_file(self, id_file):
        ...

    async def get_files(self, ids_file: list):
        ...

    async def get_task(self, id_task):
        ...
