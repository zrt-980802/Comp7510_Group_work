from kivy.metrics import dp
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu

from EndPoint import Data
import EndPoint.CheckInfo as CI
from Tools import NowTime
from Tools.Global import appData


class MD3Card(MDCard):
    title = StringProperty()
    content = StringProperty()
    uuid = StringProperty()

    def jump2Post(self, postInfo):
        print(f'postInfo:{postInfo},self.uuid:{self.uuid}')
        appData.app.show_screen('post')
        appData.postScreen.postLoad(self.uuid)


def ifTooLong(content, isTitle=False):
    changeSize = 55
    if isTitle is True:
        changeSize = 30
    if len(content) > changeSize:
        content = content[0:changeSize] + '...'
    return content


MenuListName = ['Create post', 'quit', 'Search', 'refresh', 'my post']


class ForumMainScreen(Screen):
    # name2Page = {'Homepage': '', }
    def reload(self):
        self.ids.listOfPost.clear_widgets()
        self.listOfPostLoad()

    def menuAndLoginNameLoad(self):
        # menu loading
        menu_list = [  # ['Homepage', 'home-account'],
            [MenuListName[0], 'note-plus-outline'],
            [MenuListName[4], 'menu'],
            [MenuListName[1], 'location-exit'],
        ]
        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": f"{item[0]}",
                "height": dp(56),
                # "right_icon": item[1],
                "on_release": lambda x=item[0]: self.menu_callback(x),
            } for item in menu_list
        ]
        self.menu = MDDropdownMenu(
            items=menu_items,
            width_mult=4,
        )
        # login name loading
        loginNameText = 'Traveler'
        if CI.checkLogin():
            loginNameText = appData.userInfo.user_nick_name
        self.ids.loginName.text = loginNameText
        self.ids.greetWord.text = NowTime.judgeGreetWord()

    def listOfPostLoad(self):
        postData = Data.getLatestPost()
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
                title = ifTooLong(item['post_title'], True)
                content = ifTooLong(item['post_content'], False)
                uuid = item['post_id']
                self.ids.listOfPost.add_widget(
                    MD3Card(
                        line_color=(0.2, 0.2, 0.2, 0.8),
                        style=style,
                        title=title,
                        content=content,
                        uuid=uuid,
                        md_bg_color=styles[style],
                        shadow_softness=2 if style == "elevated" else 12,
                        shadow_offset=(0, 1) if style == "elevated" else (0, 2),
                    )
                )

    def on_start(self):
        self.menu = None
        self.menuAndLoginNameLoad()
        self.listOfPostLoad()

    def callback(self, button):
        self.menu.caller = button
        self.menu.open()

    def menu_callback(self, button):
        if button == MenuListName[0]:
            if CI.checkLogin():
                appData.app.show_screen('createPost')
            else:
                self.show_dialog('Not logged in', 'Please sign in')
        if button == MenuListName[1]:
            appData.app.go_back_login()
        if button == MenuListName[2]:
            appData.app.show_screen('search')
        if button == MenuListName[3]:
            self.reload()
        if button == MenuListName[4]:
            if CI.checkLogin():
                appData.app.show_screen('myPost')
                appData.myPostScreen.listOfPostLoad()
            else:
                self.show_dialog('Not logged in', 'Please sign in')
        self.menu.dismiss()

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
