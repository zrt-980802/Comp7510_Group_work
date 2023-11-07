# -*- coding: utf-8 -*-
"""
@Time ： 2023/11/6 16:07
@Auth ： Andong
@File ：NowTime.py
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)
"""
import time
from datetime import datetime


def nowYMDHMS():
    return str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))


def nowNum():
    return str(time.time())


def str2TimeNum(datetime_str):
    datetime_object = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
    return datetime_object
