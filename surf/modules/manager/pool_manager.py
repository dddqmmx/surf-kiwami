# -*- coding: utf-8 -*-
"""
Created By      : ZedFeorius
Created Time    : 2024/12/22 23:13
File Name       : pool_manager
Last Edit Time  : 
"""
from typing import Dict, Any, Tuple

from .email_manager import EmailManager
from .user_manager import UserManager
from .server_manager import ServerManager
from surf.appsGlobal import get_logger
from surf.modules.util import BaseConsumer

_con_log = get_logger('pool_manager')


class PoolManager(object):
    def __init__(self):
        self.user_manager = UserManager()
        self.server_manager = ServerManager()
        self.email_manager = EmailManager()
        _con_log.info('PoolManager initialized.')

    async def login_user_to_pool(
            self, user_id: str,
            account: str,
            nick_name: str,
            user_info: Dict[str, Any],
            consumer: BaseConsumer) -> None:
        await self.user_manager.add_user(
            user_id=user_id,
            account=account,
            nick_name=nick_name,
            user_info=user_info,
            public_key='test',
            consumer=consumer)
        consumer.user_id = user_id

    async def log_out_user_from_pool(self, user_id: str):
        await self.user_manager.remove_user(user_id=user_id)

    async def get_email_code(self, email: str) -> Tuple[str, bool]:
        return await self.email_manager.generate_alphanumeric_code(email)
