from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List, Union, Dict

from pydantic import BaseModel, Field, model_validator

from data.settings.setting import Config

config = Config.load()

@dataclass
class ApiPoint:
    createTask: str = f"{config.api.host}/tasks.task.add.json"
    getTask: str = f"{config.api.host}/tasks.task.get.json"
    listTask: str = f"{config.api.host}/tasks.task.list.json"
    filesAttach: str = f"{config.api.host}/tasks.task.files.attach.json"
    taskGetFields: str = f"{config.api.host}/tasks.task.getFields"
    addFile: str = f"{config.api.host}/disk.storage.uploadfile.json"
    getFile: str = f"{config.api.host}/disk.file.getfields.json"
    storageGetlist: str = f"{config.api.host}/disk.storage.getlist.json"
    taskUserField: str = f"{config.api.host}/task.item.userfield.get.json"


class Group(BaseModel):
    id: int
    name: str
    opened: bool
    membersCount: int  # Приведение к формату из словаря
    image: Optional[str] = None
    additionalData: Optional[List] = []  # Приведение к формату из словаря


class User(BaseModel):
    id: int
    name: str
    link: str
    icon: Optional[str] = None
    workPosition: Optional[str] = None  # Приведение к формату из словаря


class ResponseTask(BaseModel):
    id: int = Field(..., title="ID")  # Уникальный идентификатор задачи
    parentId: Optional[int] = None  # Приведение к формату из словаря
    title: Optional[str]  # Название задачи
    description: Optional[str] = None  # Описание задачи
    mark: Optional[str] = None  # Оценка задачи
    priority: Optional[str] = '1'  # Приведение к формату из словаря (строка, а не int)
    multitask: Optional[str] = 'N'  # Флаг множественной задачи
    notViewed: Optional[str] = 'N'  # Приведение к формату из словаря
    replicate: Optional[str] = 'N'  # Флаг повторяемой задачи
    stageId: Optional[int] = None  # Приведение к формату из словаря
    createdBy: int  # Приведение к формату из словаря
    createdDate: Optional[datetime] = None  # Приведение к формату из словаря
    responsibleId: int  # Приведение к формату из словаря
    changedBy: Optional[int] = None  # Приведение к формату из словаря
    changedDate: Optional[datetime] = None  # Приведение к формату из словаря
    statusChangedBy: Optional[int] = None  # Приведение к формату из словаря
    closedBy: Optional[int] = None  # Приведение к формату из словаря
    closedDate: Optional[datetime] = None  # Приведение к формату из словаря
    activityDate: Optional[datetime] = None  # Приведение к формату из словаря
    dateStart: Optional[datetime] = None  # Приведение к формату из словаря
    deadline: Optional[datetime] = None  # Приведение к формату из словаря
    startDatePlan: Optional[datetime] = None  # Приведение к формату из словаря
    endDatePlan: Optional[datetime] = None  # Приведение к формату из словаря
    guid: Optional[str] = None  # Приведение к формату из словаря
    xmlId: Optional[str] = None  # Приведение к формату из словаря
    commentsCount: Optional[int] = 0  # Приведение к формату из словаря
    serviceCommentsCount: Optional[int] = 0  # Приведение к формату из словаря
    newCommentsCount: Optional[int] = 0  # Приведение к формату из словаря
    allowChangeDeadline: Optional[str] = 'N'  # Приведение к формату из словаря
    allowTimeTracking: Optional[str] = 'N'  # Приведение к формату из словаря
    taskControl: Optional[str] = 'N'  # Приведение к формату из словаря
    addInReport: Optional[str] = 'N'  # Приведение к формату из словаря
    forkedByTemplateId: Optional[int] = None  # Приведение к формату из словаря
    timeEstimate: Optional[str] = None  # Приведение к формату из словаря (строка, а не int)
    timeSpentInLogs: Optional[int] = None  # Приведение к формату из словаря
    matchWorkTime: Optional[str] = 'N'  # Приведение к формату из словаря
    forumTopicId: Optional[int] = None  # Приведение к формату из словаря
    forumId: Optional[int] = None  # Приведение к формату из словаря
    siteId: Optional[str] = None  # Приведение к формату из словаря
    subordinate: Optional[str] = 'N'  # Приведение к формату из словаря
    exchangeModified: Optional[datetime] = None  # Приведение к формату из словаря
    exchangeId: Optional[int] = None  # Приведение к формату из словаря
    outlookVersion: Optional[str] = None  # Приведение к формату из словаря (строка, а не int)
    viewedDate: Optional[datetime] = None  # Приведение к формату из словаря
    sorting: Optional[float] = None  # Приведение к формату из словаря
    durationPlan: Optional[int] = None  # Приведение к формату из словаря
    durationFact: Optional[int] = None  # Приведение к формату из словаря
    durationType: Optional[str] = 'days'  # Приведение к формату из словаря
    isMuted: Optional[str] = 'N'  # Приведение к формату из словаря
    isPinned: Optional[str] = 'N'  # Приведение к формату из словаря
    isPinnedInGroup: Optional[str] = 'N'  # Приведение к формату из словаря
    flowId: Optional[int] = None  # Приведение к формату из словаря
    descriptionInBbcode: Optional[str] = 'Y'  # Приведение к формату из словаря
    favorite: Optional[str] = 'N'  # Приведение к формату из словаря
    groupId: Optional[int] = None  # Приведение к формату из словаря
    auditors: Optional[List[Union[int, str]]] = []  # Приведение к формату из словаря
    accomplices: Optional[List[Union[int, str]]] = []  # Приведение к формату из словаря
    group: Optional[Union[Group, List]] = []  # Приведение к формату из словаря
    creator: Optional[User] = None  # Приведение к формату из словаря
    responsible: Optional[User] = None  # Приведение к формату из словаря
    accomplicesData: Optional[
        Union[Dict[str, User], List[User]]] = None  # Это поле может быть либо словарем, либо пустым списком
    auditorsData: Optional[
        Union[Dict[str, User], List[User]]] = None  # Это поле может быть либо словарем, либо пустым списком
    subStatus: Optional[str] = None  # Приведение к формату из словаря

    @model_validator(mode="before")
    def check_empty_accomplices_and_auditors(cls, values):
        # Если accomplicesData или auditorsData пусты, преобразуем в пустой список
        if not values.get('accomplicesData'):
            values['accomplicesData'] = []
        if not values.get('auditorsData'):
            values['auditorsData'] = []
        if not values.get('group'):
            values['group'] = []
        return values


class RequestTask(BaseModel):
    TITLE: Optional[str]  # Название задачи
    DESCRIPTION: Optional[str] = None  # Описание задачи
    RESPONSIBLE_ID: Optional[str] = "8"
    CREATED_BY: Optional[str] = "52"
    FLOW_ID: Optional[int] = 18
    UF_AUTO_474459663205: Optional[str] = None
    UF_AUTO_370133723970: Optional[str] = None
    UF_AUTO_159915603538: Optional[datetime] = None


class DataUploadFile(BaseModel):
    NAME: Optional[str]


class UploadFile(BaseModel):
    id: Optional[int] = 3
    fileContent: Optional[str]
    data: Optional[DataUploadFile]
    generateUniqueName: Optional[bool] = True


class FileDetails(BaseModel):
    ID: int
    NAME: str
    CODE: Optional[str]
    STORAGE_ID: Optional[str]
    TYPE: Optional[str]
    PARENT_ID: Optional[str]
    DELETED_TYPE: Optional[int]
    GLOBAL_CONTENT_VERSION: Optional[int]
    FILE_ID: Optional[int]
    SIZE: Optional[str]
    CREATE_TIME: Optional[datetime]
    UPDATE_TIME: Optional[datetime]
    DELETE_TIME: Optional[datetime]
    CREATED_BY: Optional[str]
    UPDATED_BY: Optional[str]
    DELETED_BY: Optional[str]
    DOWNLOAD_URL: Optional[str]
    DETAIL_URL: Optional[str]
