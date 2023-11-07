# -*- coding: utf-8 -*-
"""
@Time ： 2023/11/7 12:34
@Auth ： Andong
@File ：PostScreen.py
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)
"""
import os

from kivy.metrics import dp
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from kivymd.uix.card import MDCard
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelThreeLine
from kivymd.uix.label import MDLabel

from EndPoint import Data
from Tools.Global import appData


class MD5Card(MDCard):
    commentUserName = StringProperty()
    commentContent = StringProperty()
    commentUuid = StringProperty()

    def reply(self):
        print('reply')


class MD4Card(MDCard):
    title = StringProperty()
    content = StringProperty()
    uuid = StringProperty()


class PostScreen(Screen):

    def postLoad(self, postUuid):
        postInfo = Data.getPostInfoById(postUuid)
        commentData = Data.getLatestComment(postUuid)
        count = 0
        styles = {
            "elevated": "#f6eeee", "filled": "#f4dedc", "outlined": "#f8f5f4"
        }
        title = postInfo.post_title
        content = postInfo.post_content
        uuid = postUuid

        self.ids.postAndComment.add_widget(
            MD4Card(
                id='postCard',
                line_color=(0.2, 0.2, 0.2, 0.8),
                style='outlined',
                title=title,
                content=content,
                uuid=uuid,
                md_bg_color='#d4baf5',
                shadow_softness=2,
                shadow_offset=(0, 2)
            )
        )

        for item in commentData:
            count += 1
            style = None
            if count % 3 == 0:
                style = 'elevated'
            elif count % 3 == 1:
                style = 'filled'
            else:
                style = 'outlined'
            commentUserName = item['userInfo'].user_nick_name
            commentContent = item['commentInfo'].comment_content
            self.ids.postAndComment.add_widget(
                MD5Card(
                    line_color=(0.2, 0.2, 0.2, 0.8),
                    style=style,
                    commentUserName=commentUserName,
                    commentContent=commentContent,
                    commentUuid=postUuid,
                    md_bg_color=styles[style],
                    shadow_softness=2 if style == "elevated" else 12,
                    shadow_offset=(0, 1) if style == "elevated" else (0, 2),
                )
            )

    def on_start(self):
        self.postLoad(appData.userData.postUuid)
        print('PostScreen on_start...')
