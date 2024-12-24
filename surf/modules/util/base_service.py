# -*- coding: utf-8 -*-
"""
Created By      : ZedFeorius
Created Time    : 2024/12/21 23:07
File Name       : base_service
Last Edit Time  : 
"""
from typing import List, Union, Any

from surf.appsGlobal import logger


class ParamCheckError(Exception):
    """参数检查错误"""
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class BaseService(object):
    logger = logger

    def __init__(self):
        pass

    def param_check(self, params: List[Any], param_type: Union[List[type], type, None] = None) -> bool:
        """
        检查参数是否符合指定的类型要求或默认值有效性。

        :param params: 参数值列表
        :param param_type: 参数类型要求，可以是单一类型、类型列表或 None
        :return: 如果检查通过，返回 True；否则返回 False
        :raises ParamCheckError: 当类型验证失败或配置错误时抛出
        """
        if not isinstance(params, list):
            raise ParamCheckError(f"params should be a list, got {type(params)}")

        if param_type:
            # 检查 param_type 是否为类型列表，且长度与 params 匹配
            if isinstance(param_type, list):
                if len(param_type) != len(params):
                    raise ParamCheckError("params and param_type length mismatch")

                for i in range(len(params)):
                    if not self._is_valid_and_type(params[i], param_type[i]):
                        logger.error(f"Invalid parameter: param '{params[i]}' is either None or not of type {param_type[i]}")
                        return False

            # 检查 param_type 是否为单一类型
            elif isinstance(param_type, type):
                for param in params:
                    if not self._is_valid_and_type(param, param_type):
                        logger.error(f"Invalid parameter: param '{param}' is either None or not of type {param_type}")
                        return False

            # 如果 param_type 是其他无效值
            else:
                raise ParamCheckError(f"Invalid param_type value: {param_type}")

        else:
            # 如果未指定 param_type，检查默认值有效性
            for param in params:
                if not self._is_valid(param):
                    logger.error(f"Invalid value detected: param '{param}' is not valid.")
                    return False

        return True

    def _is_valid(self, param: Any) -> bool:
        """
        检查参数是否为有效值。

        :param param: 参数值
        :return: 如果值有效，返回 True；否则返回 False
        """
        if param is None:
            return False
        if isinstance(param, str) and param.strip() == "":
            return False
        if isinstance(param, (list, dict, set)) and len(param) == 0:
            return False
        if isinstance(param, (int, float)) and param != param:  # 检查 NaN
            return False
        return True

    def _is_valid_and_type(self, param: Any, expected_type: type) -> bool:
        """
        检查参数是否既符合指定类型又非 None。

        :param param: 参数值
        :param expected_type: 期望的类型
        :return: 如果值有效且类型正确，返回 True；否则返回 False
        """
        return param is not None and isinstance(param, expected_type)
