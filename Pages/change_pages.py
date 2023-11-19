import logging

import certifi
import os

from Pages.account.LoginScreen import LoginScreen
from Pages.account.RegisterScreen import RegisterScreen
from Pages.file.FileSelectScreen import FileSelectScreen
from Pages.forum.CreatePostScreen import CreatePostScreen
from Pages.forum.ForumMainScreen import ForumMainScreen
from Pages.forum.MyPostScreen import MyPostScreen
from Pages.forum.SearchScreen import SearchScreen
from Pages.forum.PostScreen import PostScreen
from Pages.account.ProfileScreen import ProfileScreen
from Pages.account.EditProfileScreen import EditProfileScreen

from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.utils import platform
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager

import EndPoint.CheckInfo as CI

from Tools.Global import appData

os.environ['SSL_CERT_FILE'] = certifi.where()

ch = logging.StreamHandler()
ch.setLevel(logging.WARNING)

# 记得修改尺寸
if platform in ('win', 'macosx'):
    Window.size = (414, 736)

appData.last_screens = []

# Chinese support

LabelBase.register('myFont', 'source/font/DroidSansFallback.ttf')


class MyApp(MDApp):

    def go_back_login(self):
        screenManager = appData.screenManager
        while screenManager.current != 'login':
            appData.app.go_back()
        if CI.checkLogin():
            del (appData.userInfo)

    def show_screen(self, screen_name):
        screenManager = appData.screenManager
        appData.last_screens.append(screenManager.current)
        screenManager.transition.direction = 'left'
        screenManager.current = screen_name

    def go_back(self):
        screen_name = appData.last_screens.pop()
        screenManager = appData.screenManager
        screenManager.transition.direction = 'right'
        screenManager.current = screen_name

    def build(self):
        self.title = 'Forum'

        Builder.load_file('source/kv/LoginScreen.kv')
        Builder.load_file('source/kv/RegisterScreen.kv')
        Builder.load_file('source/kv/ForumMainScreen.kv')
        Builder.load_file('source/kv/SearchScreen.kv')
        Builder.load_file('source/kv/CreatePostScreen.kv')
        Builder.load_file('source/kv/FileSelectScreen.kv')
        Builder.load_file('source/kv/PostScreen.kv')
        Builder.load_file('source/kv/MyPostScreen.kv')
        Builder.load_file('source/kv/ProfileScreen.kv')
        Builder.load_file('source/kv/EditProfileScreen.kv')

        screenManager = ScreenManager()
        screenManager.add_widget(LoginScreen(name='login'))
        screenManager.add_widget(RegisterScreen(name='register'))
        forumMainScreen = ForumMainScreen(name='mainForum')
        screenManager.add_widget(forumMainScreen)
        screenManager.add_widget(SearchScreen(name='search'))
        createPostScreen = CreatePostScreen(name='createPost')
        screenManager.add_widget(createPostScreen)
        fileSelectScreen = FileSelectScreen(name='fileSelect')
        screenManager.add_widget(fileSelectScreen)
        postScreen = PostScreen(name='post')
        screenManager.add_widget(postScreen)
        myPostScreen = MyPostScreen(name='myPost')
        screenManager.add_widget(myPostScreen)
        profileScreen = ProfileScreen(name='profile')
        screenManager.add_widget(profileScreen)
        editProfileScreen = EditProfileScreen(name='editProfile')
        screenManager.add_widget(editProfileScreen)

        appData.postScreen = postScreen
        appData.forumMainScreen = forumMainScreen
        appData.screenManager = screenManager
        appData.fileSelectScreen = fileSelectScreen
        appData.createPostScreen = createPostScreen
        appData.myPostScreen = myPostScreen
        appData.profileScreen = profileScreen
        appData.editProfileScreen = editProfileScreen
        return screenManager


appData.topic = 'forum'
appData.app = MyApp()

appData.app.run()
