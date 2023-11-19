from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog

from EndPoint import Data
from EndPoint.ForumData.UserInfo import UserInfo
from Tools.Encryption import desEncrypt
from Tools.Global import appData

class ChangePasswordScreen(Screen):
    def quit(self):
        appData.app.go_back()

    def checkPasswordInfo(self):
        old_password = self.ids.old_password_field.text
        new_password = self.ids.new_password_field.text
        re_new_password = self.ids.re_new_password_field.text
        if old_password == '' or new_password == '' or re_new_password == '':
            return [False, 'Error', 'Please fill in all blanks']
        if new_password != re_new_password:
            return [False, 'Error', 'Password mismatch']
        enPassword = desEncrypt(old_password)
        if enPassword != appData.userInfo.user_password:
            return [False, 'Error', 'Old password wrong']

        sig = [0, 0, 0, 0]
        if len(new_password) >= 8:
            for i in new_password:
                if i.islower():
                    sig[0] += 1
                if i.isupper():
                    sig[1] += 1
                if i.isdigit():
                    sig[2] += 1
                if i == '@' or i == '$' or i == '_':
                    sig[3] += 1
        else:
            return [False, 'Error', 'Password too short']

        if sum(sig) != len(new_password):
            return [False, 'Error', 'Invalid password format']

        counter = 0
        for item in sig:
            if item == 0:
                counter += 1
        if counter >= 3:
            return [False, 'Error', 'Password must contain at least 2 kinds of characters']

        return [True, 'Success', 'Password updated']

    def show_dialog(self, title, text):
        dialog = MDDialog(
            title=title,
            text=text,
            buttons=[
                MDRaisedButton(
                    text='Confirm',
                    on_press=lambda x: dialog.dismiss()),
            ]
        )
        dialog.open()

    def updatePassword(self):
        infoList = self.checkPasswordInfo()
        if not infoList[0]:
            self.show_dialog(infoList[1], infoList[2])
        else:
            self.show_dialog(infoList[1], infoList[2])
            userInfo = appData.userInfo
            userInfo.user_password = str(desEncrypt(self.ids.new_password_field.text))
            Data.updateInfo(userInfo)
            appData.app.go_back()