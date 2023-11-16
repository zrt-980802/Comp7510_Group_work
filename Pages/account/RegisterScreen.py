# -*- coding: utf-8 -*-
"""
@Time ： 2023/10/11 10:08
@Auth ： Andong
@File ：RegisterScreen.py
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)
"""
import re
import uuid
from datetime import datetime

from faker import Faker
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog

from EndPoint import Data
from EndPoint.ForumData.UserInfo import UserInfo
from Tools.Encryption import desEncrypt
from Tools.Global import appData


class RegisterScreen(Screen):
    def passwordChecker(self, password):
        flag = True
        sig = [0, 0, 0, 0]
        if len(password) >= 8:
            for i in password:
                if i.islower():
                    sig[0] += 1
                if i.isupper():
                    sig[1] += 1
                if i.isdigit():
                    sig[2] += 1
                if i == '@' or i == '$' or i == '_':
                    sig[3] += 1
        else:
            return [False, 'Password too short']

        if sum(sig) != len(password):
            return [False, 'Invalid password format']

        counter = 0
        for item in sig:
            if item == 0:
                counter += 1
        if counter >= 3:
            return [False, 'Password must contain at least 2 kinds of characters']

        return [True, 'No problem']

    def emailChecker(self, email):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if re.fullmatch(regex, email):
            return True
        else:
            return False

    def checkRegisterInfo(self):
        user_name = self.ids.user_name_field.text
        email = self.ids.email_field.text
        password = self.ids.password_field.text
        re_password = self.ids.re_password_field.text
        phone_number = self.ids.phone_number_field.text
        print(f'{user_name},{email},{password},{re_password},{phone_number}')
        if user_name == '' or email == '' or password == '' or re_password == '' or phone_number == '':
            return [False, 'Error', 'Please fill in all blanks']
        if Data.isUserNameExist(user_name)[0] is True:
            return [False, 'Error', 'Username already exists']
        if re_password != password:
            return [False, 'Error', 'Password mismatch']
        checkPasswordInfo = self.passwordChecker(password)
        if checkPasswordInfo[0]:
            if not self.emailChecker(email):
                return [False, 'Error', 'Email format error']

        return [True, 'Success', 'Welcome to the app!']

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

    def register(self):
        infoList = self.checkRegisterInfo()
        if not infoList[0]:
            self.show_dialog(infoList[1], infoList[2])
            print('register info is not correct!')
        else:
            self.show_dialog(infoList[1], infoList[2])
            userInfo = UserInfo()
            userInfo.user_id = 'user:'+str(uuid.uuid1())
            userInfo.user_name = self.ids.user_name_field.text
            faker = Faker()
            userInfo.user_nick_name = faker.name()
            userInfo.user_password = str(desEncrypt(self.ids.password_field.text))
            userInfo.user_phone_number = self.ids.phone_number_field.text
            userInfo.user_email = self.ids.email_field.text
            userInfo.user_auth_role = 0
            userInfo.user_create_time = str(datetime.now())
            Data.setInfo(userInfo)
            Data.setUserIdAndUserNameRel(userInfo.user_id, userInfo.user_name)
            appData.app.go_back()

    def cancel(self):
        appData.app.go_back()

    def clear(self):
        for index in self.ids:
            self.ids[index].text = ""
