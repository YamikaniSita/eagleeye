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
                print(DBHandler().addDisease(name, desc))
            i = i+1
        #change version hist
        curr_time = datetime.datetime.now()
        DBHandler().update_db_version(curr_time)
        return True
    def get_last_update_time(self):
        return DBHandler().get_db_version()[1]