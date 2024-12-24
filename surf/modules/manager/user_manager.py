# -*- coding: utf-8 -*-
"""
Created By      : ZedFeorius
Created Time    : 2024/12/22 1:51
File Name       : user_manager
Last Edit Time  : 
"""
from __future__ import annotations

import asyncio
import datetime
from typing import Any, Dict, Optional, TYPE_CHECKING
from surf.appsGlobal import get_logger
from surf.modules.entity import SurfUser
from surf.modules.util import BaseConsumer

_con_log = get_logger('user_manager')


class UserManager(object):
    def __init__(self):
        self._connect_users: Dict[str, SurfUser] = {}
        self._lock = asyncio.Lock()
        _con_log.info("UserManager initialized")
        asyncio.create_task(self.heartbeat_checker(), name='heartbeat_checker')

    async def add_user(self,
                       user_id: str,
                       account: str,
                       nick_name: str,
                       public_key: str,
                       consumer: BaseConsumer,
                       user_info: Dict[str, Any]) -> SurfUser:
        async with self._lock:
            if user_id in self._connect_users:
                _con_log.warning(f'User {user_id} already exist. Overwriting')
            new_user = SurfUser(
                user_id=user_id,
                account_id=account,
                nick_name=nick_name,
                public_key=public_key,
                consumer=consumer,
                user_info=user_info,
                connect_at=datetime.datetime.now()
            )
            self._connect_users[user_id] = new_user
            _con_log.info(f"User added: {new_user}")
            return new_user

    async def remove_user(self, user_id: str) -> None:
        async with self._lock:
            if user_id in self._connect_users:
                del self._connect_users[user_id]
                _con_log.info(f"User removed: {user_id}")
            else:
                _con_log.error(f"Attempted to remove non-existent user {user_id}.")

    async def get_user(self, user_id: str) -> Optional[SurfUser]:
        async with self._lock:
            return self._connect_users.get(user_id, None)

    async def get_all_users(self) -> Dict[str, SurfUser]:
        async with self._lock:
            return self._connect_users

    async def heartbeat_checker(self, interval: int = 30):
        __HEARTBEAT_TIMEOUT = 300
        while True:
            await asyncio.sleep(interval)
            async with self._lock:
                current_time = datetime.datetime.now()
                inactivate_users = [
                    user_id for user_id, user in self._connect_users.items()
                    if (current_time - user.connect_at).total_seconds() > __HEARTBEAT_TIMEOUT
                ]
                for user_id in inactivate_users:
                    await self.remove_user(user_id)
                    _con_log.info(f"User: {user_id} timed out and was removed")
