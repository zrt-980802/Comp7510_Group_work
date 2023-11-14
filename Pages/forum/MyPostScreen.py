# -*- coding: utf-8 -*-
"""
@Time ： 2023/11/14 16:11
@Auth ： Andong
@File ：MyPostScreen.py
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)
"""
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from kivymd.uix.card import MDCard

from EndPoint import Data
from Tools.Global import appData


def ifTooLong(content, isTitle=False):
    changeSize = 55
    if isTitle is True:
        changeSize = 30
    if len(content) > changeSize:
        content = content[0:changeSize] + '...'
    return content


class MD7Card(MDCard):
    myPostTitle = StringProperty()
    myPostContent = StringProperty()
    myPostUuid = StringProperty()

    def jump(self, postUuid):
        appData.app.show_screen('post')
        appData.postScreen.on_start(postUuid)

    def delete(self, postUuid):
        # delete part
        Data.deletePostByPostIdAndHide(postUuid)

        # reload part
        appData.myPostScreen.reloadList()


class MyPostScreen(Screen):
    def quit(self):
        appData.app.go_back()

    def reloadList(self):
        self.ids.listOfPost.clear_widgets()
        self.listOfPostLoad()

    def listOfPostLoad(self):
        postData = Data.getAllPostByUserId(appData.userInfo.user_id)
        count = 0
        styles = {
            "elevated": "#f6eeee", "filled": "#f4dedc", "outlined": "#f8f5f4"
        }

        if postData is not None:
            for item in postData:
                count += 1
                style = None
                if count % 3 == 0:
                    style = 'elevated'
                elif count % 3 == 1:
                    style = 'filled'
                else:
                    style = 'outlined'
                title = ifTooLong(item.post_title, True)
                content = ifTooLong(item.post_content, False)
                uuid = item.post_id
                self.ids.listOfPost.add_widget(
                    MD7Card(
                        line_color=(0.2, 0.2, 0.2, 0.8),
                        style=style,
                        myPostTitle=title,
                        myPostContent=content,
                        myPostUuid=uuid,
                        md_bg_color=styles[style],
                        shadow_softness=2 if style == "elevated" else 12,
                        shadow_offset=(0, 1) if style == "elevated" else (0, 2),
                    )
                )
