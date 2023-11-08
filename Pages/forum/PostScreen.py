# -*- coding: utf-8 -*-
"""
@Time ： 2023/11/7 12:34
@Auth ： Andong
@File ：PostScreen.py
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)
"""
import os
import uuid

from kivy.metrics import dp
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from kivymd.uix.card import MDCard
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelThreeLine
from kivymd.uix.label import MDLabel

from EndPoint import Data
from EndPoint.ForumData.CommentInfo import CommentInfo
from Tools import NowTime
from Tools.Global import appData


class MD5Card(MDCard):
    commentUserName = StringProperty()
    commentContent = StringProperty()
    commentUuid = StringProperty()


class MD4Card(MDCard):
    title = StringProperty()
    content = StringProperty()
    uuid = StringProperty()


class PostScreen(Screen):
    postUuid = None

    def quit(self):
        self.ids.postAndComment.clear_widgets()
        self.postUuid = None
        appData.app.go_back()

    def reply(self):
        print('reply')
        # 加入当前对话
        replyContent = self.ids.replyComment.text
        userInfo = appData.userInfo
        commentUserName = userInfo.user_nick_name
        commentContent = replyContent
        self.ids.postAndComment.add_widget(
            MD5Card(
                line_color=(0.2, 0.2, 0.2, 0.8),
                style='outlined',
                commentUserName=commentUserName,
                commentContent=commentContent,
                commentUuid=self.postUuid,
                md_bg_color="#f8f5f4",
                shadow_softness=2,
                shadow_offset=(0, 1),
            )
        )
        # 存入数据库
        newComment = CommentInfo()
        newComment.comment_id = str(uuid.uuid1())
        newComment.comment_content = commentContent
        newComment.comment_is_comment_to_topic = True
        newComment.comment_creator_user_id = userInfo.user_id
        newComment.comment_state = 1
        newComment.comment_create_time = NowTime.nowYMDHMS()
        newComment.comment_username = userInfo.user_name
        Data.setInfo(newComment)
        Data.setUserIdCommentIdRelationship(self.postUuid, userInfo.user_id, newComment.comment_id)

    def postLoad(self, postUuid):
        self.postUuid = postUuid
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
                line_color=(0.2, 0.2, 0.2, 0.8),
                style='elevated',
                title=str(title),
                content=str(content),
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

    def on_start(self, postUuid):
        self.postLoad(postUuid)
        print('PostScreen on_start...')
