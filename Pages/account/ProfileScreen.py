from kivy.metrics import dp
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu

from EndPoint import Data
from Tools.Global import appData

class ProfileScreen(Screen):
    def quit(self):
        appData.app.go_back()

    def jumpToEdit(self):
        appData.app.show_screen('editProfile')
        appData.editProfileScreen.getProfile()

    def getProfile(self):
        self.ids.user_name_field.text = 'Username: ' + appData.userInfo.user_name
        self.ids.user_nick_name_field.text = 'Nickname: ' + appData.userInfo.user_nick_name
        self.ids.user_phone_number_field.text = 'Phone Number: ' + appData.userInfo.user_phone_number
        self.ids.user_email_field.text = 'E-mail: ' + appData.userInfo.user_email