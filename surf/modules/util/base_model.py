# -*- coding: utf-8 -*-
"""
Created By      : ZedFeorius
Created Time    : 2024/4/18 17:25
File Name       : base_model.py
Last Edit Time  : 
"""

from .base_db_pg import BaseDBPG


class BaseModel(object):
    def __init__(self):
        self._pg = BaseDBPG()
