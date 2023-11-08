# -*- coding: utf-8 -*-
"""
@Time ： 2023/11/3 21:54
@Auth ： Andong
@File ：SearchScreen.py
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)
"""
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.relativelayout import MDRelativeLayout

from EndPoint import Data
from Tools.Global import appData

limitationOfShow = 10


class MD6Card(MDCard):
    searchTitle = StringProperty()
    searchContent = StringProperty()
    searchUuid = StringProperty()

    def jump(self, postUuid):
        appData.app.show_screen('post')
        appData.postScreen.on_start(postUuid)


def ifTooLong(content, isTitle=False):
    changeSize = 55
    if isTitle is True:
        changeSize = 30
    if len(content) > changeSize:
        content = content[0:changeSize] + '...'
    return content


class SearchScreen(Screen):

    def __init__(self, **kw):
        super().__init__(**kw)

    def search(self):
        keyword = self.ids.searchTextField.text
        postData = Data.getPostByKeyword(keyword)
        count = 0
        styles = {
            "elevated": "#f5e5ba", "filled": "#f5e5ba", "outlined": "#d4baf5"
        }
        for item in postData:

            if count == limitationOfShow:
                break
            count += 1
            style = None
            if count % 3 == 0:
                style = 'elevated'
            elif count % 3 == 1:
                style = 'filled'
            else:
                style = 'outlined'
            title = ifTooLong(item['post_title'], True)
            content = ifTooLong(item['post_content'], False)
            uuid = item['post_id']
            print(title + ' ' + content)
            self.ids.searchResult.add_widget(
                MD6Card(
                    line_color=(0.2, 0.2, 0.2, 0.8),
                    style=style,
                    searchTitle=title,
                    searchContent=content,
                    searchUuid=uuid,
                    md_bg_color=styles[style],
                    shadow_softness=2 if style == "elevated" else 12,
                    shadow_offset=(0, 1) if style == "elevated" else (0, 2),
                )
            )
