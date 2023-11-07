import certifi
import os

from Pages.account.LoginScreen import LoginScreen
from Pages.account.RegisterScreen import RegisterScreen
from Pages.file.FileSelectScreen import FileSelectScreen
from Pages.forum.CreatePostScreen import CreatePostScreen
from Pages.forum.ForumMainScreen import ForumMainScreen
from Pages.forum.SearchScreen import SearchScreen
from Pages.forum.PostScreen import PostScreen

os.environ['SSL_CERT_FILE'] = certifi.where()

from kivy.core.window import Window
from kivy.utils import platform
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager

from Tools.Global import appData

# 记得修改尺寸
if platform in ('win', 'macosx'):
    Window.size = (414, 636)

appData.last_screens = []


class MyApp(MDApp):

    def go_back_login(self):
        screenManager = appData.screenManager
        while screenManager.current != 'login':
            appData.last_screens.pop()

    def show_screen(self, screen_name):
        screenManager = appData.screenManager

        ### remember the last screen
        appData.last_screens.append(screenManager.current)
        print(appData.last_screens)

        ### set transition effect
        screenManager.transition.direction = 'left'

        ### change screen
        screenManager.current = screen_name

    def go_back(self):
        ### get the name of the last screen
        screen_name = appData.last_screens.pop()
        print(appData.last_screens)

        screenManager = appData.screenManager

        ### set transition effect
        screenManager.transition.direction = 'right'

        ### change screen
        screenManager.current = screen_name

    ### The app starts with a single screen. The screen defination is loaded from the KV file
    def build(self):
        self.title = 'Forum'

        ### load KV files individually
        # Builder.load_file('source/kv/LoginScreen.kv')
        # Builder.load_file('source/kv/RegisterScreen.kv')
        Builder.load_file('source/kv/ForumMainScreen.kv')
        # Builder.load_file('source/kv/SearchScreen.kv')
        # Builder.load_file('source/kv/CreatePostScreen.kv')
        # Builder.load_file('source/kv/FileSelectScreen.kv')
        Builder.load_file('source/kv/PostScreen.kv')

        screenManager = ScreenManager()
        # screenManager.add_widget(LoginScreen(name='login'))
        # screenManager.add_widget(RegisterScreen(name='register'))
        screenManager.add_widget(ForumMainScreen(name='mainForum'))
        # screenManager.add_widget(SearchScreen(name='search'))
        # screenManager.add_widget(CreatePostScreen(name='createPost'))
        # screenManager.add_widget(FileSelectScreen(name='fileSelect'))
        postScreen = PostScreen(name='post')
        screenManager.add_widget(postScreen)
        appData.postScreen = postScreen

        appData.screenManager = screenManager

        return screenManager


### appData is a global name defined in Global.py
### Now appData.app refers to the app
### We can add anything to appData and get them back in different py files
appData.topic = 'forum'
appData.app = MyApp()
appData.app.run()

appData.isTest = True
