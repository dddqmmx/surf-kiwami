# -*- coding: utf-8 -*-
"""
Created By      : ZedFeorius
Created Time    : 2024/12/21 21:43
File Name       : user_service
Last Edit Time  : 
"""
import traceback
from typing import Dict, Union, Any, List, Tuple

import json

from surf.appsGlobal import logger, setResult, errorResult
from surf.modules.consumer.models import UserModel
from surf.modules.util.base_service import BaseService


class UserService(BaseService):
    def __init__(self):
        super().__init__()
        self.__userModel = UserModel()

    def login(self, text_data: Dict[str, Any]) -> tuple[str, Dict[str, Any] | None]:
        """
        :param text_data:
            {
                'account' : str,
                'password' : str
            }
        :return: json
        """
        user: Dict[str, str] = {}
        try:
            account: Union[str, None] = text_data['data'].get('account', None)
            password: Union[str, None] = text_data['data'].get('password', None)
            if self.param_check(params=[account, password], param_type=str):
                res = self.__userModel.login(account=account, password=password)
                user = res[0] if res else {}
                if user:
                    return setResult('login', user, 'user'), user
                else:
                    return errorResult('login', '用户不存在或密码错误', 'user'), user
        except Exception as e:
            logger.error(f"login error:{e}\n{traceback.format_exc()}")
            return errorResult('login', u'登录失败', 'user'), user

    def get_user_info(self, text_data: Dict[str, Any]) -> dict[str, Any] | str:
        """
        get user info
        :param text_data: json
        :return: json
        """
        user_id: str | None = text_data['data'].get('user_id', None)
        if self.param_check(params=[user_id]):
            try:
                data = self.__userModel.get_user_data_by_id(user_id=user_id)
                if str(text_data['command']).startswith('inner_'):
                    return data[0]
                return setResult(text_data['command'], data[0], 'user') if data\
                    else errorResult(text_data['command'], 'un-existence user', text_data['path'])
            except Exception as e:
                logger.error(f"get data of user:{user_id} failed:{e}")
                return errorResult(text_data['command'], 'server busy', text_data['path'])
        else:
            logger.error(f"invalid user_id:{user_id}")
            return errorResult(text_data['command'], 'invalid user_id:', text_data['path'])

    def check_user_exits(self, text_data: Dict[str, Any]) -> str | List[str]:
        email = text_data['data'].get('email', '')
        if self.param_check(params=[email], param_type=str):
            if self.__userModel.check_user_exist_by_email(email=email):
                return errorResult(text_data['command'], 'user exist', text_data['path'])
            else:
                return [email]
        else:
            logger.error(f"invalid email: {email}")
            return errorResult(text_data['command'], 'invalid email', text_data['path'])
