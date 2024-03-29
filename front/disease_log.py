from kivy.storage.jsonstore import JsonStore
from kivy.network.urlrequest import UrlRequest
from front_db_scripts import DBHandler
import json
from datetime import datetime
class DiseaseLog:
    def addToLog(self, detectedLabel):
        r = False
        user = JsonStore('user_account.json')
        if(user.exists('user_profile')):
            id = user.get('user_profile')['session_id']
            coords = user.get('user_profile')['coords']
            district = user.get('user_profile')['district']
            time = datetime.now()
            return DBHandler().saveLog(id, coords, detectedLabel, district, time)
        return r
    def getLog(self, filter_by_not_uploaded = False):
        return DBHandler().loadLogs(filter_by_not_uploaded)
