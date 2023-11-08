from kivy.metrics import dp
from kivy.properties import StringProperty
from kivy.uix.image import AsyncImage
from kivy.uix.screenmanager import Screen
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.menu import MDDropdownMenu
from kivymd.font_definitions import theme_font_styles

from EndPoint import Data
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


ManuListName = ['Create post', 'quit', 'Search', 'refresh']


class ForumMainScreen(Screen):
    # name2Page = {'Homepage': '', }
    def reload(self):
        self.ids.listOfPost.clear_widgets()
        self.listOfPostLoad()

    def menuLoad(self):
        menu_list = [  # ['Homepage', 'home-account'],
            [ManuListName[0], 'note-plus-outline'],
            [ManuListName[1], 'location-exit']]
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

    def listOfPostLoad(self):
        postData = Data.getLatestPost(4)
        count = 0
        styles = {
            "elevated": "#f6eeee", "filled": "#f4dedc", "outlined": "#f8f5f4"
        }

        if postData is not None:
            for item in postData.values():
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
        self.menuLoad()
        self.listOfPostLoad()

    def callback(self, button):
        self.menu.caller = button
        self.menu.open()

    def menu_callback(self, button):
        if button == ManuListName[0]:
            appData.app.show_screen('createPost')
        if button == ManuListName[1]:
            appData.app.go_back_login()
        if button == ManuListName[2]:
            appData.app.show_screen('search')
        if button == ManuListName[3]:
            self.reload()
        self.menu.dismiss()
