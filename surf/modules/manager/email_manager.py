# -*- coding: utf-8 -*-
"""
Created By      : ZedFeorius
Created Time    : 2024/12/25 16:43
File Name       : email_manager
Last Edit Time  : 
"""
import asyncio
import datetime
import secrets
import string
from typing import Dict, Tuple

from django.utils import timezone

from surf.appsGlobal import get_logger, HEARTBEAT_TIMEOUT

_con_log = get_logger('email_manager')


class EmailManager(object):
    def __init__(self):
        self._generated_code: Dict[str, Dict[str, int]] = {}
        self._lock = asyncio.Lock()
        _con_log.info('EmailManager initialized')
        asyncio.create_task(self.heartbeat_checker(), name="email_manager_heartbeat_checker")

    async def generate_alphanumeric_code(self, email: str, length=8, code_timeout=300) -> Tuple[str, bool]:
        """
        生成一个指定长度的字母数字混合验证码。如果当前没有验证码
        或者验证码已超时，则生成一个新的验证码。

        参数:
            length (int): 验证码的长度。默认值为8。
            code_timeout (int): 验证码的有效时间（秒）。默认值为300秒（5分钟）。

        返回:
            str: 当前有效的验证码。
            bool: 是否需要重新发送邮件
        """
        async with self._lock:
            flag = False
            current_time = timezone.now()

            # 判断是否需要生成新验证码
            needs_new_code = (
                not self._generated_code.get(email, False) or
                (current_time - list(self._generated_code[email].values())[0]) > datetime.timedelta(seconds=code_timeout)
            )

            if needs_new_code:
                flag = True
                self._generated_code[email] = {self._generate_code(length): current_time}

            return list(self._generated_code[email].keys())[0], flag

    @staticmethod
    def _generate_code(length) -> str:
        """
        生成一个指定长度的字母数字混合验证码。

        参数:
            length (int): 验证码的长度。

        返回:
            str: 生成的验证码。
        """
        characters = string.ascii_letters + string.digits
        return ''.join(secrets.choice(characters) for _ in range(length))

    async def remove_email_code(self, email: str) -> None:
        async with self._lock:
            if email in self._generated_code:
                del self._generated_code[email]
                _con_log.info(f'Email code {email} removed')
            else:
                _con_log.error(f"Attempted to remove non-existent email {email}")

    async def heartbeat_checker(self, interval: int = 30):
        while True:
            await asyncio.sleep(interval)
            async with self._lock:
                current_time = timezone.now()
                timeout_code_emails = [
                    email for email, v in self._generated_code.items()
                    if (current_time - int(list(v.values())[0])).total_seconds() > HEARTBEAT_TIMEOUT
                ]
                for email in timeout_code_emails:
                    await self.remove_email_code(email)
