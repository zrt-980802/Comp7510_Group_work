from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog

from EndPoint import Data
from Tools.Encryption import desEncrypt
from Tools.Global import appData


class LoginScreen(Screen):
    def guestLogin(self):
        appData.app.show_screen('mainForum')
        appData.forumMainScreen.on_start()

    def login(self):
        userName = self.ids.user_name_field.text
        password = self.ids.password_field.text
        checkBox = self.ids.is_remember_for_next_time
        if checkBox.state == 'down':
            userName = 'admin'
            password = 'admin123'
            pass
        else:
            self.show_dialog('wrong', 'Please confirm compliance with the treaty')
            return

        if userName == '' or password == '':
            self.show_dialog('wrong', 'can\'t be emtpy!')
            return
        else:
            request_rel = Data.isUserNameExist(userName)

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
        appData.userInfo = userInfo
        appData.app.show_screen('mainForum')
        appData.forumMainScreen.on_start()

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
