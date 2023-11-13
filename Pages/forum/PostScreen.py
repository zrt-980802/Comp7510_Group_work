# -*- coding: utf-8 -*-
"""
@Time ： 2023/11/7 12:34
@Auth ： Andong
@File ：PostScreen.py
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)
"""
import uuid

from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.fitimage import FitImage

from EndPoint import Data
from EndPoint.ForumData.CommentInfo import CommentInfo
import EndPoint.CheckInfo as CI

from Tools import NowTime
from Tools.Global import appData


class MD5Card(MDCard):
    commentUserName = StringProperty()
    commentContent = StringProperty()
    commentUuid = StringProperty()


class MD4Card(MDCard):
    postTitle = StringProperty()
    postContent = StringProperty()
    postUuid = StringProperty()


class PostScreen(Screen):
    postUuid = None

    def quit(self):
        self.ids.postAndComment.clear_widgets()
        self.postUuid = None
        appData.app.go_back()

    def reply(self):
        if CI.checkLogin() is False:
            self.show_dialog('Not logged in', 'Please sign in')
            return

        # do reply
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
        postCard = MD4Card(
            id='postCard',
            line_color=(0.2, 0.2, 0.2, 0.8),
            style='elevated',
            postTitle=title,
            postContent=content,
            postUuid=postUuid,
            md_bg_color='#d4baf5',
            shadow_softness=2,
            shadow_offset=(0, 2)
        )
        self.ids.postAndComment.add_widget(postCard)

        if postInfo.post_annex is not None:
            print(postInfo.post_annex)
            postCard.add_widget(
                FitImage(
                    source=postInfo.post_annex[1],
                    radius=[12, 12, 12, 12],
                    size_hint_x=.25,

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

    def show_dialog(self, title, text):
        dialog = MDDialog(
            title=title,
            text=text,
            buttons=[
                MDRaisedButton(
                    text='confirm',
                    on_press=lambda x: dialog.dismiss()),
            ]
        )
        dialog.open()
