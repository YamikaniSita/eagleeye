from re import S
from tkinter import ON
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.storage.jsonstore import JsonStore
from kivy.clock import Clock
from kivy.properties import ObjectProperty
import urllib
prev_screen = None
class SplashScreen(Screen):
    def on_enter(self, *args):
        store = JsonStore('user_account.json')
        self.userRegistered = False
        if(store.exists('user_profile')):
            self.userRegistered = True
        Clock.schedule_once(self.switch, 10)
    def switch(self, dt):
        print(self.userRegistered)
        if(self.userRegistered == False):
            self.manager.current = 'login'
        # else:``
        #     pass
class LoginScreen(Screen):
    user_password = ObjectProperty()
    user_phone = ObjectProperty()
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.busy = False
    def loginUser(self):
        print(self.busy)
        print('[EagleEye] Login Initiated')
        self.busy = True
        print(self.busy)
    def switchToRegister(self):
        self.manager.current = "registerScreen"
    def switchToDataPolicy(self):
        self.manager.prev_screen = "login"
        self.manager.current = "DataPolicyScreen"
class RegisterScreen(Screen):
    user_pw = ObjectProperty()
    user_name = ObjectProperty()
    user_district = ObjectProperty()
    user_pn = ObjectProperty()
    def switchToLogin(self):
        self.manager.current = "login"
    def switchToDataPolicy(self):
        self.manager.prev_screen = "registerScreen"
        self.manager.current = "DataPolicyScreen"
class DataPolicyScreen(Screen):
    def on_back(self):
        self.manager.current = self.manager.prev_screen
class WindowManager(ScreenManager):
    pass
class EagleEyeApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Orange"
EagleEyeApp().run()