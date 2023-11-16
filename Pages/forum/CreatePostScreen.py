# -*- coding: utf-8 -*-
"""
@Time ： 2023/11/6 12:13
@Auth ： Andong
@File ：CreatePostScreen.py
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)
"""
import os
import uuid

from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog

from EndPoint import Data
from EndPoint.ForumData.PostInfo import PostInfo
from Tools import NowTime
from Tools.Global import appData
import EndPoint.CheckInfo as CI


class CreatePostScreen(Screen):
    def addAnnexFirst(self):
        appData.app.show_screen('fileSelect')

    def addAnnexSecond(self):
        if appData.fileSelect is not None:
            file = appData.fileSelect
            path = file['folder'] + "\\" + file['files'][0]
            self.ids.createPostFileSelect.text = file['files'][0]
            self.ids.createPostFileSelect.secondary_text = path

    def deleteAnnex(self):
        self.ids.createPostFileSelect.text = 'File name'
        self.ids.createPostFileSelect.secondary_text = 'File path'

    def createPost(self):
        if CI.checkLogin() is False:
            self.show_dialog('Not logged in', 'Please sign in')
            appData.app.go_back()
            return

        title = self.ids.titleField.text
        content = self.ids.contentField.text
        path = self.ids.createPostFileSelect.secondary_text
        userInfo = appData.userInfo
        newPost = PostInfo()
        newPost.post_id = 'post:' + str(uuid.uuid1())
        newPost.post_state = '0'
        newPost.post_title = title
        newPost.post_content = content
        newPost.post_create_time = NowTime.nowYMDHMS()
        newPost.post_create_time_num = NowTime.nowNum()
        newPost.post_creator_user_id = userInfo.user_id

        if (path != '' and path != 'File Path' and path is not None) and os.path.exists(path):
            try:
                newPost.post_annex = Data.uploadFile(path)
            except Exception:
                newPost.post_annex = None
        else:
            self.deleteAnnex()
            if not os.path.exists(path):
                self.show_dialog('wrong', 'Invalid file address')

        try:
            Data.setInfo(newPost)
            Data.setUserIdPostIdRelationshipByUserId(newPost.post_creator_user_id, newPost.post_id)
        except Exception:
            Data.deleteInfo(newPost)
        appData.app.go_back()
        appData.forumMainScreen.reload()

        # clear
        self.ids.titleField.text = ''
        self.ids.contentField.text = ''
        self.ids.createPostFileSelect.text = ''
        self.ids.createPostFileSelect.secondary_text = ''

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
