from kivy.metrics import dp
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu

from EndPoint import Data
from Tools.Global import appData

class EditProfileScreen(Screen):
    def quit(self):
        appData.app.go_back()

    def getProfile(self):
        self.ids.userName.text = appData.userInfo.user_name
        self.ids.userNickName.text = appData.userInfo.user_nick_name
        self.ids.userPhoneNumber.text = appData.userInfo.user_phone_number
        self.ids.userEmail.text = appData.userInfo.user_email