# -*- coding: utf-8 -*-
"""
Created By      : ZedFeorius
Created Time    : 2024/12/21 20:56
File Name       : routing
Last Edit Time  : 
"""
from django.urls import re_path
from surf.modules.consumer import *

url = [
    re_path(r'ws/surf/$', SurfConsumer.as_asgi())
]