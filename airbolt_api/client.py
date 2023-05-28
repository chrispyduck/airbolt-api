import json
import logging
from base64 import b64encode
from datetime import datetime
from typing import List, Optional
from urllib.parse import urljoin

from aiohttp import ClientSession
from classes import (DeviceHistoryPage, FoundDevice, HistoryEntry, LoginResult,
                     UserInfo)
from pydantic import parse_raw_as

logger: logging.Logger = logging.getLogger("airbolt_api.client")


class AirboltClient:
    BASE_URL = "https://airboltapiconnect.com/api/"

    _session: ClientSession
    _username: str
    _password: str
    _login_result: LoginResult

    def __init__(self, user_id: str, password: str):
        self._session = ClientSession()
        self._session.headers.update({
            "Accept": "application/json",
            "Authorization": "",
            "Content-Type": "application/json; charset=utf-8",
        })
        self._username = user_id
        self._password = password

    async def __aenter__(self) -> "AirboltClient":
        return self

    async def __aexit__(self, *args):
        await self.close()

    async def close(self):
        await self._session.close()

    async def _get(self, path: str) -> str:
        response = await self._session.get(urljoin(AirboltClient.BASE_URL, path))
        if response.status == 200:
            return await response.text()
        
        raise response.raise_for_status()
    
    async def _post(self, path: str, body: dict) -> str:
        response = await self._session.post(urljoin(AirboltClient.BASE_URL, path), json=body)
        if response.status == 200:
            return await response.text()
        
        raise response.raise_for_status()


    async def login(self) -> LoginResult:
        raw_response = await self._post("login", {
            "username": self._username,
            "password": self._password,
            "twoFactorCode": "",
        })
        self._login_result = LoginResult.parse_raw(raw_response)

        self._session.headers.update({
            "Accept": "application/json",
            "Authorization": self._login_result.auth_header,
        })

        logger.info(f"Authenticated as {self._login_result.username}")

        return self._login_result
        

    async def get_user_info(self) -> UserInfo:
        raw_data = await self._get("users/me")
        return UserInfo.parse_raw(raw_data)
    
    async def find_devices(self) -> List[FoundDevice]:
        raw_data = await self._get(f"devices/find/{self._login_result.id}?page=0&perPage=999")
        return parse_raw_as(List[FoundDevice], raw_data)
    
    async def get_device_history_page(self, device_uuid: str, page: int = 1, page_size: int = 10) -> List[DeviceHistoryPage]:
        raw_data = await self._get(f"history/find/device/{device_uuid}?page={page}&perPage={page_size}")
        return parse_raw_as(DeviceHistoryPage, raw_data)
