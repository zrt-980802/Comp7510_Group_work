from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog

from EndPoint import Data
from Tools.Encryption import desEncrypt, desDecrypt
from Tools.Global import appData


class LoginScreen(Screen):
    def login(self):
        userName = self.ids.user_name_field.text
        password = self.ids.password_field.text
        request_rel = Data.isUserNameExit(userName)
        if request_rel[0] is False:
            self.show_dialog('wrong', 'Username not exits!')
            return
        userId = request_rel[1]
        userInfo = Data.getUserInfoById(userId)
        enPassword = desEncrypt(password)
        if enPassword != userInfo.user_password:
            self.show_dialog('wrong', 'Username or password is wrong!')
            return
        self.show_dialog('success', 'login successful!')
        appData.app.show_screen('main_forum')

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
