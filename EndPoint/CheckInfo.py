# -*- coding: utf-8 -*-
"""
@Time ： 2023/11/6 15:53
@Auth ： Andong
@File ：CheckInfo.py
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)
"""
from Tools.Global import appData


def checkLogin():
    userInfo = appData.userData.userInfo
    if userInfo is None:
        return False
