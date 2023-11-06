# -*- coding: utf-8 -*-
"""
@Time ： 2023/11/6 16:07
@Auth ： Andong
@File ：NowTime.py
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)
"""
import time


def nowYMDHMS():
    return str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))


def nowNum():
    return str(time.time())
