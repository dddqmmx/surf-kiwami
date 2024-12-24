# -*- coding: utf-8 -*-
"""
Created By      : ZedFeorius
Created Time    : 2024/12/21 20:57
File Name       : surf_consumer
Last Edit Time  : 
"""
import json

from typing import Union, Dict, Callable
from surf.appsGlobal import logger, setResult, errorResult, REQUEST_FORMAT
from surf.modules.consumer.services import UserService
from surf.modules.manager.pool_manager import PoolManager
from surf.modules.util import BaseConsumer


class SurfConsumer(BaseConsumer):
    def __init__(self, **kwargs):
        super(SurfConsumer, self).__init__(**kwargs)
        self.userPool = PoolManager()
        self.user_id: Union[str, None] = None
        self.service_dict = {
            'user': UserService()
        }
        self.func_dict: Dict[str, Dict[str, Callable[[str], any]]] = {
            "user": {
                "login": self.login
            }
        }

    async def connect(self):
        try:
            await self.accept()
            logger.info(f"WebSocket connected: {self.scope['client'][1]}")
        except Exception as e:
            logger.error(f"Error during connect: {e}")
            await self.close()

    async def disconnect(self, close_code):
        await self.userPool.log_out_user_from_pool(self.user_id)
        logger.info(f"WebSocket disconnected: {self.scope['client'][1]}, Close code: {close_code}")

    async def receive(self, text_data=None, bytes_data=None):
        text_data = json.loads(text_data)
        command = text_data['command']
        # path = self.scope['url_route']['kwargs']['path']
        path = text_data['path']
        if path in self.func_dict.keys() and command in self.func_dict[path].keys():
            await self.func_dict[path].get(command)(text_data)

    async def login(self, text_data=None, bytes_data=None):
        respond_json, user = self.service_dict['user'].login(text_data)
        if not user:
            await self.send(respond_json)
        else:
            request_json = REQUEST_FORMAT
            request_json['path'] = 'user'
            request_json['command'] = 'inner_get_user_info'
            request_json['data'] = {
                'user_id': user['id']
            }
            user_info = self.service_dict['user'].get_user_info(request_json)
            await self.userPool.login_user_to_pool(
                user_id=user['id'],
                account=user_info['account'],
                nick_name=user_info['nickname'],
                user_info=user_info['user_info'],
                consumer=self)
            await self.send(respond_json)
