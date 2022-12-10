from kivy.storage.jsonstore import JsonStore
from kivymd.uix.snackbar import Snackbar

class LanguageManager:
    def getPrompt(self, phrase_title):
        profile = JsonStore('user_account.json')
        lang = "eng" #default
        if profile.exists('user_profile'):
            lang = profile.get('user_profile')['lang']
        phrases = JsonStore('languages.json')
        return phrases[0][phrase_title][lang]
    def switchLanguage(self, lang):
        store = JsonStore('user_account.json')
        coords = store['user_profile']['coords']
        district = store['user_profile']['district']
        session_id = store['user_profile']['session_id']
        store.put('user_profile', coords=coords, district=district, lang=lang, session_id=session_id)
        Snackbar(text="Language changed...restart application").open()
        return True        
    def getUserLanguage(self):
        profile = JsonStore('user_account.json')
        lang = "eng" #default
        if profile.exists('user_profile'):
            lang = profile.get('user_profile')['lang']
        return lang