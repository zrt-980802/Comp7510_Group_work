from kivy.metrics import dp
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.menu import MDDropdownMenu
from kivymd.font_definitions import theme_font_styles

from EndPoint import Data


class MD3Card(MDCard):
    title = StringProperty()
    content = StringProperty()
    uuid = StringProperty()

    def jump(self, pageName, listInfo):
        print(f'pageName{pageName},listOfInfo{listInfo}')


def ifTooLong(content, isTitle=False):
    changeSize = 55
    if isTitle is True:
        changeSize = 30
    if len(content) > changeSize:
        content = content[0:changeSize] + '...'
    return content


class ForumMainScreen(Screen):
    # name2Page = {'Homepage': '', }

    def menuLoad(self):
        menu_list = [['Homepage', 'home-account'],
                     ['post', 'note-plus-outline'],
                     ['quit', 'location-exit']]
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
        post_data = Data.getLatestPost(4)
        title_theme = 'Primary'
        content_theme = 'Custom'
        count = 0
        styles = {
            "elevated": "#f6eeee", "filled": "#f4dedc", "outlined": "#f8f5f4"
        }
        for item in post_data.values():
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

    def __init__(self, **kw):
        super().__init__(**kw)
        self.menu = None
        self.menuLoad()
        self.listOfPostLoad()

    def callback(self, button):
        self.menu.caller = button
        self.menu.open()

    def menu_callback(self, button):
        # self.menu.caller = button
        # self.menu.open()
        print(button)
