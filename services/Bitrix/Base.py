import logging
from typing import Any

import aiohttp
import requests

logger = logging.getLogger(__name__)


class BaseClient:
    def __init__(self):
        self.__headers = {
            "Content-Type": "application/json"
        }

    def _prepare_params(self, params: dict[str, Any], prev: str = "") -> str:
        """
        Transform list of parameters to a valid bitrix array.

        Parameters
        ----------
            params (dict): Dictionary of parameters
            prev (str): Previous key

        Returns
        -------
            str: Prepared parameters
        """
        ret = ""
        if isinstance(params, dict):
            for key, value in params.items():
                if isinstance(value, dict):
                    if prev:
                        key = "{0}[{1}]".format(prev, key)
                    ret += self._prepare_params(value, key)
                elif (isinstance(value, list) or isinstance(value, tuple)) and len(value) > 0:
                    for offset, val in enumerate(value):
                        if isinstance(val, dict):
                            ret += self._prepare_params(
                                val, "{0}[{1}][{2}]".format(prev, key, offset)
                            )
                        else:
                            if prev:
                                ret += "{0}[{1}][{2}]={3}&".format(prev, key, offset, val)
                            else:
                                ret += "{0}[{1}]={2}&".format(key, offset, val)
                else:
                    if prev:
                        ret += "{0}[{1}]={2}&".format(prev, key, value)
                    else:
                        ret += "{0}={1}&".format(key, value)
        return ret

    async def _post(self, url: str, params: dict | list[dict]):
        params = self._prepare_params(params)
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            response = await session.post(url=url, data=params)
            if response.status == 200:
                logger.info(f"Successfully response {url}, status: {response.status}")
            else:
                logger.info(f"Error response {url}, status: {response.status}")
            data = await response.json()
            await session.close()
        return data

    def _get(self, url: str, params: dict | list[dict] = None):
        # Подготовка параметров
        params = self._prepare_params(params)
        # logger.info(params)
        # Выполняем GET-запрос
        try:
            response = requests.get(url, params=params)

            # Проверяем статус ответа
            if response.status_code == 200:
                data = response.json()
                logger.info(f"Successfully got response from {url}, status: {response.status_code}\nparams: {params}")
            else:
                data = response.text
                logger.info(f"Error in response from {url}, status: {response.status_code}\nparams: {params}")

        except requests.exceptions.RequestException as e:
            logger.info(f"An error occurred while making the request: {e}")
            data = None

        # Возвращаем данные
        return data

    async def _get_async(self, url: str, params: dict | list[dict] = None):
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector()) as session:
            # Выполняем GET-запрос
            params = self._prepare_params(params)
            async with session.get(url=url, params=params) as response:
                # Проверяем статус ответа
                if response.status == 200:
                    data = await response.json()
                    logger.info(f"Successfully get response from {url}, status: {response.status}\nparams: {params}")
                else:
                    data = await response.text()
                    logger.info(f"Error in response from {url}, status: {response.status}\nparams: {params}")

                # Читаем данные JSON из ответа
                return data
