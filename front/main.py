# -*- coding utf-8 -*-
# Yamikani Sita
# Mzuzu University, ICT Department
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.storage.jsonstore import JsonStore
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.list import OneLineListItem, OneLineAvatarListItem
from kivy.clock import Clock
from kivy.properties import ObjectProperty, StringProperty
from kivy.network.urlrequest import UrlRequest
import json
from kivymd.uix.button import MDRaisedButton

from front_db_scripts import DBHandler
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import AsyncImage
from kivy.logger import Logger
import datetime
from kivy.clock import Clock, mainthread
from changelog import Changelog
from disease_log import DiseaseLog
from lang_manager import LanguageManager
from time import time
import math
from plyer import sms, filechooser
from PIL import Image                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        

prev_screen = None
class SplashScreen(Screen):
    state = StringProperty('')
    def on_enter(self, *args):
        Logger.info('Loading profile')
        store = JsonStore('user_account.json')
        # store.delete('user_profile')
        #127 for local runs, 192 for LAN comment out the idle one

        # self.manager.url = 'http://127.0.0.1:5000'
        self.manager.url = 'http://192.168.43.230:5000'

        if(store.exists('user_profile')):
            Logger.info('Profile Found')
            self.userRegistered = True
             #check changelog updates if connected
            last_update_time = Changelog().get_last_update_time()
            params = json.dumps({'app_last_update': last_update_time})
            headers = {'Content-Type':'application/json'}
            req = UrlRequest(self.manager.url+'/app/changelog/get', req_body=params, on_success=self.installChangeLog, on_progress=self.progress, on_failure=self.failed, on_error=self.err, timeout=5)
            print("Network req triggered")
        else:
            Logger.info('Profile not found')
            self.userRegistered = False
            Clock.schedule_once(self.switch, 20)
            # self.switch()
    def switch(self, *args):
        if(self.userRegistered == False):
            self.manager.current = 'LoginScreen'
        else:
            self.manager.current = 'HomeScreen'
    def installChangeLog(self, request, result):
        if len(result['change_log']) > 0:
            self.state = "Installing updates"
        Logger.info(result)
        Changelog().install(result['change_log'])
        self.manager.current = 'HomeScreen'
    def progress(self, request, current_size, total_size):
        Logger.info("{}/{}".format(current_size, total_size))
    def failed(self, request, result):
        Logger.info(result)

        self.switch()
    def err(self, request, result):
        Logger.info(result)
        self.switch()
class LoginScreen(Screen):
    def on_enter(self, *args):
        req = UrlRequest('https://ipinfo.io/json?token=39895a94007e4d', on_success=self.loginUser, on_progress=self.progress, on_failure=self.failed)
        Logger.info('Attempting to connect to IpInfo')
    def loginUser(self, req, response):
        Logger.info('IpInfo acquired')
        self.coords = response['loc']
        self.district = response['city']
        params = json.dumps({'district': self.district})
        headers = {'Content-Type':'application/json'}
        print(params)
        req = UrlRequest(self.manager.url+'/app/new-session', on_success=self.success, on_progress=self.progress, on_failure=self.failed, req_body=params, req_headers=headers)
    def success(self, req, result):
        Logger.info(result)
        if result['success']:
            store = JsonStore('user_account.json')
            session_id = result['session_id']
            store.put('user_profile', coords=self.coords, district=self.district, session_id = session_id, lang = 'eng')
            self.manager.current = 'HomeScreen'
        else:
            Snackbar(text="Setup failed for unknown reason...retry.").open()
    def failed(self, req, err):
        Snackbar(text="Network/server error").open()
    def progress(self, request, current_size, total_size):
        Logger.info('Request progress detected @ {}/{}'.format(current_size, total_size))
        
class HomeScreen(Screen):
    userLocation = StringProperty('')
    temp = StringProperty('')
    lang_manager = LanguageManager()
    dialog = None
    def on_enter(self, *args):
        store = JsonStore('user_account.json')
        locale = "{}, Malawi".format(store.get('user_profile')['district'])
        lat = store.get('user_profile')['coords'].split(',')[0]
        long = store.get('user_profile')['coords'].split(',')[1]
        self.userLocation = locale
        url = "https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&units=metric&appid=5fe9e0dac8d9f901c5ac48e7dbc19c04".format(lat, long)
        req = UrlRequest(url, on_success=self.success, on_failure=self.failed)
        d_log = DiseaseLog()
        pending_logs = d_log.getLog(True)
        if(len(pending_logs) > 0):
            # uplooad
            params = json.dumps({'logs': pending_logs})
            req = UrlRequest(self.manager.url+'/logs/add', req_body=params, on_success=self.clearPending)
            print("Network req triggered logs")
    def clearPending(self, req, response):
        # send messages
        messages = response['messages']
        recipients = response['recipients']
        for i in range(0, len(messages)):
            msg = messages[i]
            msg1, msg2 =  msg[:160], msg[160:320] # truncate sms limits
            recipients_l = recipients[i]
            for j in range(0, len(recipients_l)):
                print("sending sms to", recipients_l[j]['phoneNumber'])
                print(msg2)
                try:
                    sms.send(recipient = recipients_l[j]['phoneNumber'], message = msg1)
                    sms.send(recipient = recipients_l[j]['phoneNumber'], message = msg2)
                except:
                    print("SMS Send failed")
        DBHandler().clearPending()
    def success(self, req, response):
        print(response)
        self.temp = str(int(response['main']['temp']))+u"\u00B0C"
    def failed(self, req, error):
        print(error)
    def switchToProfile(self):
        self.manager.current = "ProfileScreen"
    def switchToKBHome(self):
        self.manager.current = "KBHomeScreen"
    def showPopup(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title = "[color=ff0101]Menu",
                type = "simple",
                items = [
                    OneLineAvatarListItem(text=self.lang_manager.getPrompt('add_client'), on_press=self.openAddClient),
                    OneLineAvatarListItem(text=self.lang_manager.getPrompt('refresh_locale'), on_press=self.refreshLocation)
                ]
            )
        self.dialog.open()
    def openAddClient(self, instance):
        self.dialog.dismiss()
        self.manager.current = "AddSMSClient"
    def refreshLocation(self, instance):
        self.dialog.dismiss()
        req = UrlRequest('https://ipinfo.io/json?token=39895a94007e4d', on_success=self.setNewLocation, on_failure=self.refreshFailed)
    def setNewLocation(self, req, response):
        self.coords = response['loc']
        self.district = response['city']
        store = JsonStore('user_account.json')
        lang = store['user_profile']['lang']
        session_id = store['user_profile']['session_id']
        store.put('user_profile', coords=self.coords, district=self.district, lang=lang, session_id=session_id)
        Snackbar(text="Location refreshed to {} coordinates: {}. Restart app to reflect.".format(self.district, self.coords)).open()
    def refreshFailed(self):
        Snackbar(text="Couldnt fetch current location. Retry later.").open()
    def on_enter_camera(self, ic):
        self.manager.current = "CameraScreen"
    def switchToSettings(self):
        self.manager.current = "SettingsScreen"
    def goToWeather(self):
        self.manager.current = "WeatherScreen"
        
class ProfileScreen(Screen):
    user_district = StringProperty('')
    pNumber = StringProperty()
    user_name = StringProperty()
    def on_enter(self, *args):
        store = JsonStore("user_account.json")
        session_id = store.get('user_profile')['session_id']
        print(self.manager.url)
        req = UrlRequest(self.manager.url+"/app/msgs/{}".format(session_id), timeout=10, on_cancel=self.cancelled, on_success=self.success, on_failure=self.failed)
    def success(self, req, response):
        self.user_name = response['profile'][0]['name']
        self.pNumber = response['profile'][0]['pNumber']
        self.user_district = response['profile'][0]['district']
    def failed(self, req, error):
        Snackbar(text="Network error.").open()
    def cancelled(self, req):
        Snackbar(text="Network error.").open()
    def on_back(self):
        self.manager.current = "HomeScreen"

class KBHomeScreen(Screen):
    lang_manager = LanguageManager()
    def on_enter(self, *args):
        self.ids.container.clear_widgets()
        res = DBHandler().getDiseaseList(self.lang_manager.getUserLanguage())
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
    def launch_search(self):
        content_cls = Content()
        self.dialog = MDDialog(
                        title = '[color=ff0101]Search',
                        type='custom',
                        height = "400",
                        auto_dismiss=True,
                        size_hint=(.7, .6),
                        content_cls=content_cls,
                        buttons = [MDRaisedButton(text='Search', on_release=lambda x: self.search(x, content_cls))]
                        )
        self.dialog.open()
    def search(self, instance, content_cls):
        field = content_cls.ids.symptoms
        entered_ = field._get_text()
        symptoms_ = entered_.split(',')
        res = DBHandler().searchSymptoms(symptoms_)
        if len(res) > 0:
            self.ids.container.clear_widgets()
        for x in range(len(res)):
            text = res[x][1]
            id = res[x][0]
            self.ids.container.add_widget(
            OneLineListItem(text=f"{text}", id=str(id), on_press=self.clk)
        )
        Snackbar(text="{} disease(s) found.".format(len(res))).open()
        self.dialog.dismiss()
class DiseaseScreen(Screen):
    diseaseName = StringProperty("")
    diseaseDesc = StringProperty("")
    lang_manager = LanguageManager()
    db = DBHandler()
    def on_enter(self, *args):
        self.diseaseName = self.manager.disease_name
        info = self.db.getDiseaseInfo(self.manager.disease_id)
        self.diseaseDesc = info[0][2]
        self.manager.imageSource = info[0][3]
        avail_langs = info[0][6]
        self.manager.diseaseName = self.diseaseName
        symptoms = self.db.getDiseaseSymptoms(self.manager.disease_id, avail_langs)
        controls = self.db.getDiseaseControls(self.manager.disease_id, avail_langs)
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

class CameraScreen(Screen):
    #crashes on PC
    lessons = []
    current_lesson = 0
    normalized_result = StringProperty("")
    def on_enter(self):
        Clock.schedule_once(self.start_camera, .5)
        self.lessons = ["For more accurate diagnosis place the suspected leaf on a surface with same colour.", "Only capture a single leaf at a time for better accuracy", "Please place the camera above the leaf and capture the entire leaf and make sure there are no foreign objects in camera view."]
        self.dialog = MDDialog(
                        title = '[color=ff0101]Tutorial',
                        type='custom',
                        height = "400",
                        auto_dismiss=True,
                        size_hint=(.7, .6),
                        text= "[color=000000]"+self.lessons[0],
                        buttons = [MDRaisedButton(text='Next', on_release=lambda x: self.next(x))]
                        )
        if DBHandler().hasUsedDiagnosis() == False:
            self.dialog.open()
    def next(self, instance):
        if self.current_lesson < len(self.lessons)-1:
            self.current_lesson = self.current_lesson + 1
            self.dialog.text = "[color=000000]"+self.lessons[self.current_lesson]
        else:
            self.dialog.dismiss()
    def start_camera(self, *largs):
        self.ids.camera.play = True
        from tflwrapper.tfl_android import TFLWrapperAndroid
        self.tflite = TFLWrapperAndroid(
            "data/pba_quantized/model.tflite",
            "data/pba_quantized/labels.txt",
            on_detect=self.on_tflite_detect)
    def pick_from_device(self):
        print("[STATUS] pick_from_device triggered")
        filechooser.open_file(on_selection = self.diagnose_from_file)
    def diagnose_from_file(self, selection):
        img = Image.open(selection[0])
        w, h = img.size
        self.tflite.async_detect(img, w, h)
    def on_back(self):
        self.manager.current = "HomeScreen"
    def on_camera_texture(self, ic):
        camera = self.ids.camera._camera
        pixels = camera._fbo.pixels
        w, h = camera.resolution
        self.tflite.async_detect(pixels, w, h)

    @mainthread
    def on_tflite_detect(self, result):
        print(result)
        self.result = result
        labels = self.tflite.get_labels_with_value(result)
        top_label = None
        top_conf_ = None
        for label, value in labels:
            if value > .8:
                top_conf_ = value
                top_label = label
        if top_label is None:
            Snackbar(text="No object detected in picture. Retake image.").open()
        elif top_label == "Others":
            Snackbar(text="Image has no tomato leaf. Please retake.").open()
        else:
            self.manager.detected_label = top_label
            self.manager.detected_conf_ = top_conf_
            self.manager.current = "DiagnosisResults"
    def detect(self, *largs):
        timer = time()
        camera = self.ids.camera._camera
        w, h = camera.resolution
        pixels = camera._fbo.pixels
        self.result = self.tfl.detect(pixels, w, h)

class DiagnosisResults(Screen):
    lang_manager = LanguageManager()
    detected_label = StringProperty("")
    detected_conf_ = StringProperty("")
    command = StringProperty("View Diagnosis")

    disease_= None
    def on_enter(self):
        self.detected_label = self.manager.detected_label
        if self.detected_label == 'Healthy':
            self.command = "Go To Home"
        self.detected_conf_ = str(math.ceil(self.manager.detected_conf_*100))
        self.disease_ = DiseaseLog().addToLog(self.detected_label)
    def on_back(self):
        self.manager.current = "HomeScreen"
    def view_disease(self):
        if self.detected_label == 'Healthy':
            self.manager.current = "HomeScreen"
        else:
            self.manager.disease_id = self.disease_["id"]
            self.manager.disease_name = self.disease_["disease"]
            self.manager.current = "DiseaseScreen"  

class AddSMSClient(Screen):
    client_name = ObjectProperty()
    client_phone = ObjectProperty()
    # def on_enter(self):
    #     recipient = "0994437644"
    #     message = "Hey Beautiful, your boyfriend loves you."
    #     sms.send(recipient = recipient, message = message)
    def add_sms_client(self):
        client_name = self.client_name.text
        client_phone = self.client_phone.text
        store = JsonStore('user_account.json')
        user_locale = store.get('user_profile')['district']
        params = json.dumps({'name': client_name, 'district': user_locale,'phoneNumber':client_phone})
        req = UrlRequest(self.manager.url+'/app/sms/add_client', req_body=params, on_success=self.success, on_failure = self.failed)
    def success(self, request, response):
        Snackbar(text="Client successfully added").open()
    def failed(self, request, response):
        Snackbar(text="Failed to add client").open()
    def on_back(self):
        self.manager.current = "HomeScreen"
    
class SettingsScreen(Screen):
    lang_manager = LanguageManager()
    def on_back(self):
        self.manager.current = "HomeScreen"
    def switchToLanguageSettings(self):
        self.manager.current = "LanguageSettings"
class LanguageSettings(Screen):
    lang_manager = LanguageManager()
    def on_back(self):
        self.manager.current = "SettingsScreen"



class Item(OneLineListItem):
    divider = None
class Content(BoxLayout):
    lang_manager = LanguageManager()
class ImageViewer(BoxLayout):
    pass
class WindowManager(ScreenManager):
    pass
class EagleEyeApp(MDApp):
    def build(self):
        self.store = JsonStore('user_account.json')
        self.theme_cls.primary_palette = "Orange"
EagleEyeApp().run()
