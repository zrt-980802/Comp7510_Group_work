# -*- coding: utf-8 -*-
"""
@Time ： 2023/11/6 12:21
@Auth ： Andong
@File ：FileSelectScreen.py
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)
"""
from kivy.uix.screenmanager import Screen
from Tools.Global import appData


class FileSelectScreen(Screen):
    def show_selected(self):
        fileList = self.ids.fileList
        selected = fileList.get_selected()
        print('selected:', selected)

    def select_callback(self):
        fileList = self.ids.fileList
        selected = fileList.get_selected()

        if len(selected['files']) != 0:
            appData.fileSelect = selected
        appData.createPostScreen.addAnnexSecond()
        appData.app.go_back()
