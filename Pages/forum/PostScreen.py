# -*- coding: utf-8 -*-
"""
@Time ： 2023/11/7 12:34
@Auth ： Andong
@File ：PostScreen.py
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)
"""
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from kivymd.uix.card import MDCard

from EndPoint import Data
from Tools.Global import appData


class MD5Card(MDCard):
    commentUserName = StringProperty()
    commentContent = StringProperty()
    commentUuid = StringProperty()

    def reply(self):
        print('reply')


class PostScreen(Screen):
    def postLoad(self,postUuid):
        commentData = Data.getLatestComment(4,postUuid)
        count = 0
        styles = {
            "elevated": "#f6eeee", "filled": "#f4dedc", "outlined": "#f8f5f4"
        }
        for item in commentData.values():
            count += 1
            style = None
            if count % 3 == 0:
                style = 'elevated'
            elif count % 3 == 1:
                style = 'filled'
            else:
                style = 'outlined'
            title = item['post_title']
            content = item['comment_content']
            uuid = item['post_id']
            self.ids.postAndComment.add_widget(
                MD5Card(
                    line_color=(0.2, 0.2, 0.2, 0.8),
                    style=style,
                    commentUserName=title,
                    content=content,
                    commentUuid=uuid,
                    md_bg_color=styles[style],
                    shadow_softness=2 if style == "elevated" else 12,
                    shadow_offset=(0, 1) if style == "elevated" else (0, 2),
                )
            )

    def __init__(self, **kw):
        super().__init__(**kw)
        self.postLoad(appData.userData.postUuid)
