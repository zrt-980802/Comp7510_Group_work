# -*- coding: utf-8 -*-
"""
@Time ： 2023/11/6 12:13
@Auth ： Andong
@File ：CreatePostScreen.py
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)
"""
import uuid

from kivy.uix.screenmanager import Screen

from EndPoint import Data
from EndPoint.ForumData.PostInfo import PostInfo
from Tools import NowTime
from Tools.Global import appData
import EndPoint.CheckInfo as CI


class CreatePostScreen(Screen):
    def createPost(self):
        if CI.checkLogin() is False:
            appData.app.go_back_login()

        title = self.ids.titleField
        content = self.ids.contentField
        userInfo = appData.userData.userInfo
        newPost = PostInfo()
        newPost.post_id = 'post:' + str(uuid.uuid1())
        newPost.post_state = 0
        newPost.post_title = title
        newPost.post_content = content
        newPost.post_create_time = NowTime.nowYMDHMS()
        newPost.post_create_time_num = NowTime.nowNum()
        newPost.post_creator_user_id = userInfo.user_id
        # newPost.post_annex
        Data.setInfo(newPost)
        appData.app.go_back()
