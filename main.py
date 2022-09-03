# -*- coding utf-8 -*-
from re import S
from tkinter import ON
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.storage.jsonstore import JsonStore
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.list import OneLineListItem
from kivy.clock import Clock
from kivy.properties import ObjectProperty, StringProperty
from kivy.network.urlrequest import UrlRequest
import json
from front_db_scripts import DBHandler
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelThreeLine
from kivymd.uix.label import MDLabel

prev_screen = None
class SplashScreen(Screen):
    def on_enter(self, *args):
        store = JsonStore('user_account.json')
        if(store.exists('user_profile')):
            self.userRegistered = True
        else:
            self.userRegistered = False
        Clock.schedule_once(self.switch, 10)
    def switch(self, dt):
        store = JsonStore('user_account.json')
        if(self.userRegistered == False):
            self.manager.current = 'login'
        else:
            self.manager.current = 'HomeScreen'
class LoginScreen(Screen):
    user_password = ObjectProperty()
    user_phone = ObjectProperty()
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.busy = False
    def getUserLocation(self):
        req = UrlRequest('https://ipinfo.io/json?token=39895a94007e4d', on_success=self.loginUser, on_failure=self.failed)
    def loginUser(self, req, response):
        self.coords = response['loc']
        self.district = response['city']
        params = json.dumps({'pNumber': self.user_phone.text, 'password':self.user_password.text})
        headers = {'Content-Type':'application/json'}
        req = UrlRequest('http://127.0.0.1:5000/login', on_success=self.success, on_failure=self.failed, req_body=params, req_headers=headers)
    def success(self, req, result):
        if result['success']:
            store = JsonStore('user_account.json')
            store.put('user_profile', coords=self.coords, district=self.district, pNumber=self.user_phone.text)
            self.manager.current = 'HomeScreen'
        else:
            Snackbar(text="Authentication failed. Details entered not known, check please.").open()
    def failed(self, req, err):
        Snackbar(text="Network/server error").open()
    def switchToRegister(self):
        self.manager.current = "registerScreen"
    def switchToDataPolicy(self):
        self.manager.prev_screen = "login"
        self.manager.current = "DataPolicyScreen"
class RegisterScreen(Screen):
    user_password = ObjectProperty()
    user_name = ObjectProperty()
    user_phone = ObjectProperty()
    def switchToLogin(self):
        self.manager.current = "login"
    def switchToDataPolicy(self):
        self.manager.prev_screen = "registerScreen"
        self.manager.current = "DataPolicyScreen"
    def getUserLocation(self):
        req = UrlRequest('https://ipinfo.io/json?token=39895a94007e4d', on_success=self.registerUser, on_failure=self.failed)
    def registerUser(self, req, response):
        self.coords = response['loc']
        self.district = response['city']
        params = json.dumps({'name': self.user_name.text, 'district': self.district, 'password': self.user_password.text, 'pNumber': self.user_phone.text})
        headers = {'Content-Type': 'application/json'}
        req = UrlRequest('http://127.0.0.1:5000/register', on_success=self.success, on_failure=self.failed, req_body=params, req_headers=headers)
    def success(self, req, result):
        print(result)
        if result['success']:
            store = JsonStore('user_account.json')
            store.put('user_profile', coords=self.coords, district=self.district, pNumber=self.user_phone.text)
            self.manager.current = 'HomeScreen'
        else:
            Snackbar(text="Registration failed, phone number may already be in use.").open()
    def failed(self, req, err):
        Snackbar(text="Network/server error").open()
class DataPolicyScreen(Screen):
    def on_back(self):
        self.manager.current = self.manager.prev_screen
class HomeScreen(Screen):
    userLocation = StringProperty('')
    temp = StringProperty('')
    def on_enter(self, *args):
        store = JsonStore('user_account.json')
        locale = "{}, Malawi".format(store.get('user_profile')['district'])
        lat = store.get('user_profile')['coords'].split(',')[0]
        long = store.get('user_profile')['coords'].split(',')[1]
        self.userLocation = locale
        url = "https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&units=metric&appid=5fe9e0dac8d9f901c5ac48e7dbc19c04".format(lat, long)
        req = UrlRequest(url, on_success=self.success, on_failure=self.failed)
    def success(self, req, response):
        self.temp = str(int(response['main']['temp']))
    def failed(self, req, error):
        print(error)
    def switchToProfile(self):
        self.manager.current = "ProfileScreen"
    def switchToKBHome(self):
        self.manager.current = "KBHomeScreen"
class ProfileScreen(Screen):
    user_district = StringProperty('')
    pNumber = StringProperty()
    user_name = StringProperty()
    def on_enter(self, *args):
        store = JsonStore("user_account.json")
        pNumber = store.get('user_profile')['pNumber']
        req = UrlRequest("http://127.0.0.1:5000/profile/{}".format(pNumber), on_success=self.success, on_failure=self.failed)
    def success(self, req, response):
        self.user_name = response['profile'][0]['name']
        self.pNumber = response['profile'][0]['pNumber']
        self.user_district = response['profile'][0]['district']
    def failed(self, req, error):
        Snackbar(text="Network error.").open()
    def on_back(self):
        self.manager.current = "HomeScreen"

class KBHomeScreen(Screen):
    def on_enter(self, *args):
        self.ids.container.clear_widgets()
        res = DBHandler().getDiseaseList()
        for x in range(len(res)):
            text = res[x][1]
            id = res[x][0]
            self.ids.container.add_widget(
            OneLineListItem(text=f"{text}", id=str(id), on_press=self.clk)
        )
    def on_back(self):
        self.manager.current = "HomeScreen"
    def clk(self, instance):
        self.manager.disease_id = instance.id
        self.manager.disease_name = instance.text
        self.manager.current = "DiseaseScreen"
class DiseaseScreen(Screen):
    diseaseName = StringProperty("")
    diseaseDesc = StringProperty("")
    db = DBHandler()
    def on_enter(self, *args):
        self.diseaseName = self.manager.disease_name
        info = self.db.getDiseaseInfo(self.manager.disease_id)
        self.diseaseDesc = info[0][2]
        self.manager.imageSource = info[0][3]
        self.manager.diseaseName = self.diseaseName
        symptoms = self.db.getDiseaseSymptoms(self.manager.disease_id)
        controls = self.db.getDiseaseControls(self.manager.disease_id)
        chemicals = self.db.getDiseaseChemicals(self.manager.disease_id)
        self.ids.symptoms_list.clear_widgets()
        self.ids.controls_list.clear_widgets()
        self.ids.chemicals_list.clear_widgets()
        for i in range(len(symptoms)):
            symptom = symptoms[i][0]
            self.ids.symptoms_list.add_widget(
            MDLabel(text=u"\u2022 {}".format(symptom), size_hint_y=None)
            )
        for i in range(len(controls)):
            control = controls[i][1]
            self.ids.controls_list.add_widget(
            MDLabel(text=u"\u2022 {}".format(control), size_hint_y=None)
            )
        for i in range(len(chemicals)):
            chemical = chemicals[i][1]
            self.ids.chemicals_list.add_widget(
            MDLabel(text=u"\u2022 {}\u2122".format(chemical), size_hint_y=None)
            )
    def on_back(self):
        self.manager.current = "KBHomeScreen"
    def switchToImage(self):
        self.manager.current = "DiseaseImageScreen"
class DiseaseImageScreen(Screen):
    imageSource = StringProperty('')
    caption = StringProperty('')
    def on_enter(self, *args):
        self.imageSource = self.manager.imageSource
        self.caption = self.manager.diseaseName
    def on_back(self):
        self.manager.current = "DiseaseScreen"
class WindowManager(ScreenManager):
    pass
class EagleEyeApp(MDApp):
    def build(self):
        self.store = JsonStore('user_account.json')
        self.theme_cls.primary_palette = "Orange"
EagleEyeApp().run()