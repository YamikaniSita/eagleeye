from re import S
from tkinter import ON
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.storage.jsonstore import JsonStore
from kivy.clock import Clock
from kivy.properties import ObjectProperty
import urllib
from kivy.network.urlrequest import UrlRequest
import json

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
        # else:
        #     pass
class LoginScreen(Screen):
    user_password = ObjectProperty()
    user_phone = ObjectProperty()
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.busy = False
    def loginUser(self):
        params = json.dumps({'pNumber': self.user_phone.text, 'password':self.user_password.text})
        headers = {'Content-Type':'application/json'}
        req = UrlRequest('http://127.0.0.1:5000/login', on_success=self.success, on_failure=self.failed, req_body=params, req_headers=headers)
        print(req)
    def success(self, req, result):
        print(result)
    def failed(self, req, err):
        print(err, req)
    def switchToRegister(self):
        self.manager.current = "registerScreen"
    def switchToDataPolicy(self):
        self.manager.prev_screen = "login"
        self.manager.current = "DataPolicyScreen"
class RegisterScreen(Screen):
    user_password = ObjectProperty()
    user_name = ObjectProperty()
    user_district = ObjectProperty()
    user_phone = ObjectProperty()
    def switchToLogin(self):
        self.manager.current = "login"
    def switchToDataPolicy(self):
        self.manager.prev_screen = "registerScreen"
        self.manager.current = "DataPolicyScreen"
    def registerUser(self):
        params = json.dumps({'name': self.user_name.text, 'district': self.user_district.text, 'password': self.user_password.text, 'pNumber': self.user_phone.text})
        headers = {'Content-Type': 'application/json'}
        print(params)
        req = UrlRequest('http://127.0.0.1:5000/register', on_success=self.success, on_failure=self.failed, req_body=params, req_headers=headers)
        print(req)
    def success(self, req, result):
        print(result)
    def failed(self, req, err):
        print(err, req)
class DataPolicyScreen(Screen):
    def on_back(self):
        self.manager.current = self.manager.prev_screen
class WindowManager(ScreenManager):
    pass
class EagleEyeApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Orange"
EagleEyeApp().run()