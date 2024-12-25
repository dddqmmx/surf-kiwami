# -*- coding: utf-8 -*-
"""
Created By      : ZedFeorius
Created Time    : 2024/3/26 17:27
File Name       : appsGloble.py
Last Edit Time  : 
"""
import json
import logging
import os
from logging.handlers import TimedRotatingFileHandler


def getPlatformPath():
    cur_path = os.path.dirname(os.path.abspath(__file__))  # 当前文件路径
    cur_path_list = cur_path.split(os.sep)  # 按文件夹炸开
    platform_path = os.sep.join(cur_path_list[0:4]) if os.sep.join(cur_path_list[0:4]) != cur_path else os.sep.join(
        cur_path_list[0:3])  # 取前俩文件夹
    return platform_path


def getAppName():
    curr = os.path.dirname(os.path.abspath(__file__))
    app_name = curr.split("/")[-1] if curr.split("/")[-1] != curr else curr.split("\\")[-1]
    return app_name


APPNAME = getAppName()
PLATFROMPATH = getPlatformPath()
APPHOME = os.path.join(PLATFROMPATH, APPNAME)
CONFIGHOME = os.path.join(APPHOME, "config")


def get_logger(logfile=APPNAME):
    """获取日志句柄的方法"""
    logger = logging.getLogger(logfile)
    logger.setLevel(logging.DEBUG)
    logroot = os.path.join(APPHOME, 'logs')

    if not os.path.exists(logroot):
        os.mkdir(logroot)
    filehandle = TimedRotatingFileHandler(os.path.normpath(logroot + "/" + \
                                                           logfile + ".log"), 'midnight', encoding='utf-8', delay=True)
    filehandle.suffix = "%Y-%m-%d"
    filehandle.setLevel(logging.DEBUG)
    consolehandle = logging.StreamHandler()
    consolehandle.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    filehandle.setFormatter(formatter)
    consolehandle.setFormatter(formatter)
    logger.addHandler(filehandle)
    logger.addHandler(consolehandle)
    return logger


def setResult(command, data, path, extra_col=None, log='') -> str:
    if not isinstance(extra_col, list):
        extra_col = []
    result = {
        "command": str(command),
        "path": path,
        "messages": []
    }
    if data is False:
        result['status'] = False
        result['msg'] = '执行失败！'
    else:
        for col in extra_col:
            result.update({k: v for k, v in col.items()})
        result['status'] = True
        result['messages'] = data
        result['msg'] = '执行成功！'
    # 添加审计日志编辑内容
    if log != '':
        result['log'] = log
    print(json.dumps(result))
    return json.dumps(result)


def errorResult(command, error_msg, path, log=''):
    result = {
        "command": str(command),
        "path": path,
        "messages": False,
        "msg": str(error_msg)
    }
    # 添加审计日志编辑内容
    if log != '':
        result['log'] = log
    print(json.dumps(result))
    return json.dumps(result)


logger = get_logger()

HEARTBEAT_TIMEOUT = 300

CHAT_TEMP = {
    "_id": "",
    "_index": "chat_message",
    "_source": {
        "chat_id": "",
        "type": "",
        "content": "",
        "user_id": "",
        "chat_time": ""
    }
}

USER_ROLE_PERMISSIONS = {
    "owner": [0],
    "admin": [1],
    "member": [2, 5, 601, 701]
}

DEFAULT_PERMISSION_SETTINGS = {
    '2': None,
    "3": None,
    '5': None,
    '6': None,
    '601': None,
    '701': None,
    '702': None,
    '70302': None,
    '8': None,
    '114514': None
}

REQUEST_FORMAT = {
    "path": None,
    "command": None,
    "request_id": None,
    "data": {}
}
