import re
import uuid
from datetime import datetime

from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog

from EndPoint import Data
from EndPoint.ForumData.UserInfo import UserInfo
from Tools.Global import appData

class EditProfileScreen(Screen):
    def quit(self):
        appData.app.go_back()

    def getProfile(self):
        self.ids.user_name_field.text = appData.userInfo.user_name
        self.ids.user_nick_name_field.text = appData.userInfo.user_nick_name
        self.ids.user_phone_number_field.text = appData.userInfo.user_phone_number
        self.ids.user_email_field.text = appData.userInfo.user_email

    def emailChecker(self, email):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if re.fullmatch(regex, email):
            return True
        else:
            return False

    def checkNewProfileInfo(self):
        user_name = self.ids.user_name_field.text
        user_nick_name = self.ids.user_nick_name_field.text
        user_phone_number = self.ids.user_phone_number_field.text
        user_email = self.ids.user_email_field.text
        if user_name == '' or user_nick_name == '' or user_phone_number == '' or user_email == '':
            return [False, 'Error', 'Please fill in all blanks']
        if (user_name != appData.userInfo.user_name) & (Data.isUserNameExist(user_name)[0] == True):
            return [False, 'Error', 'Username already exists']
        if not self.emailChecker(user_email):
            return [False, 'Error', 'Email format error']

        return [True, 'Success', 'Profile updated']

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

    def updateProfile(self):
        infoList = self.checkNewProfileInfo()
        if not infoList[0]:
            self.show_dialog(infoList[1], infoList[2])
        else:
            self.show_dialog(infoList[1], infoList[2])
            userInfo = UserInfo()
            userInfo.user_id = appData.userInfo.user_id
            userInfo.user_name = self.ids.user_name_field.text
            userInfo.user_nick_name = self.ids.user_nick_name_field.text
            userInfo.user_phone_number = self.ids.user_phone_number_field.text
            userInfo.user_email = self.ids.user_email_field.text
            Data.updateUserIdAndUserNameRel(userInfo.user_id, userInfo.user_name, appData.userInfo.user_name)
            Data.updateInfo(userInfo)
            appData.userInfo = userInfo
            appData.profileScreen.getProfile()
            appData.forumMainScreen.on_start()
            appData.app.go_back()