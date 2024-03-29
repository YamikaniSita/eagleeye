from front_db_scripts import DBHandler
import datetime
class Changelog:
    def install(self, changelog):
        i = 0
        while i < len(changelog):
            el = changelog[i]
            if el['type'] == 'new_disease':
                name = el['values']['name']
                desc = el['values']['desc']
                name_ch = el['values']['name_ch']
                desc_ch = el['values']['desc_ch']
                langs = el['values']['langs']
                print(DBHandler().addDisease(name, desc, name_ch, desc_ch, langs))
            elif el['type'] == 'new_symptom':
                new_symptom = el['values']['name']
                disease_name = el['values']['disease_key']
                lang = el['values']['lang']
                DBHandler().addSymptom(new_symptom, disease_name, lang)
            elif el['type'] == 'new_control':
                new_control = el['values']['control']
                disease_name = el['values']['disease_key']
                lang = el['values']['lang']
                DBHandler().addControl(new_control, disease_name, lang)
            elif el['type'] == 'new_chemical':
                new_chemical = el['values']['chemical_name']
                dosage = el['values']['dosage']
                disease_name = el['values']['disease_key']
                DBHandler().addChemical(new_chemical, dosage, disease_name)
            i = i+1
        #change version hist
        if len(changelog) > 0:
            curr_time = datetime.datetime.now()
            DBHandler().update_db_version(curr_time)
        return True
    def get_last_update_time(self):
        return DBHandler().get_db_version()[1]