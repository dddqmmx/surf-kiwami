# -*- coding: utf-8 -*-
"""
Created By      : ZedFeorius
Created Time    : 2024/12/24 1:16
File Name       : surf_user
Last Edit Time  : 
"""
from __future__ import annotations

import datetime
from dataclasses import dataclass
from typing import Dict, Any
from surf.modules.util import BaseConsumer


@dataclass
class SurfUser(object):
    user_id: str
    account_id: str
    nick_name: str
    public_key: str
    consumer: BaseConsumer
    user_info: Dict[str, Any]
    connect_at: datetime.datetime
