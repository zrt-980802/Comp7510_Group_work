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


def judgeGreetWord():
    hour = int(time.localtime().tm_hour)
    if 5 <= hour <= 11:
        return 'Good morning'
    if 12 <= hour <= 12:
        return 'Good noon!'
    if 13 <= hour <= 17:
        return 'Good afternoon!'
    if 18 <= hour <= 23:
        return 'Good evening!'
    return 'Good dawn!'

def nowYMDHMS():
    return str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))


def nowNum():
    return str(time.time())


def str2TimeNum(datetime_str):
    datetime_object = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
    return datetime_object
