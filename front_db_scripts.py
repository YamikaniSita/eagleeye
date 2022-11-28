import sqlite3
import datetime
from lang_mananager import LanguageManager

class DBHandler:
    conn = sqlite3.connect('frontdb.db')
    c = conn.cursor()
    def getDiseaseList(self):
        self.c.execute("SELECT * FROM diseases")
        records = self.c.fetchall()
        return records
    def getDiseaseInfo(self, id):
        self.c.execute("SELECT * FROM diseases WHERE _id = {}".format(id))
        data = self.c.fetchall()
        return data
    def getDiseaseSymptoms(self, id):
        self.c.execute("SELECT name FROM symptoms WHERE disease_id = {}".format(id))
        return self.c.fetchall()
    def getDiseaseControls(self, id):
        self.c.execute("SELECT * FROM controls WHERE disease_id = {}".format(id))
        return self.c.fetchall()
    def getDiseaseChemicals(self, id):
        self.c.execute("SELECT * FROM chemicals WHERE disease_id = {}".format(id))
        return self.c.fetchall()
    def searchSymptoms(self, symptoms):
        results = None
        query = ""
        if len(symptoms) > 0:
            query = "select * from diseases where _id in (select disease_id from symptoms where name like '%{}%')".format(symptoms[0])
            if len(symptoms) > 1:
                for i in range(len(symptoms)-1):
                    query = query + " or _id in (select disease_id from symptoms where name like '%{}%')".format(symptoms[i+1])
            self.c.execute(query)
            results = self.c.fetchall()
        return results
    def addDisease(self, name, desc):
        self.c.execute("INSERT INTO diseases (name, desc) VALUES ('{}', '{}')".format(name, desc))
        return self.conn.commit()
    def update_db_version(self, curr):
        q = "UPDATE db_version SET release_date='{}'".format(datetime.datetime.strftime(curr, "%m/%d/%Y, %H:%M:%S"))
        self.c.execute(q)
        return self.conn.commit()
    def get_db_version(self):
        self.c.execute("SELECT * FROM db_version")
        return self.c.fetchone()
    def addSymptom(self, new_symptom, disease_name):
        q = "SELECT _id FROM diseases WHERE name = '{}'".format(disease_name)
        self.c.execute(q)
        result = self.c.fetchall()[0][0]
        q = "INSERT INTO symptoms (name, disease_id) VALUES ('{}', {})".format(new_symptom, result)
        self.c.execute(q)
        return self.conn.commit()
    def addControl(self, new_control, disease_name):
        q = "SELECT _id FROM diseases WHERE name = '{}'".format(disease_name)
        self.c.execute(q)
        result = self.c.fetchall()[0][0]
        q = "INSERT INTO controls (control, disease_id) VALUES ('{}', {})".format(new_control, result)
        self.c.execute(q)
        return self.conn.commit()
    def addChemical(self, chemical_name, dosage, disease_name):
        q = "SELECT _id FROM diseases WHERE name = '{}'".format(disease_name)
        self.c.execute(q)
        result = self.c.fetchall()[0][0]
        q = "INSERT INTO chemicals (chemical_name, dosage, disease_id) VALUES ('{}', '{}',{})".format(chemical_name, dosage, result)
        self.c.execute(q)
        return self.conn.commit()
    def hasUsedDiagnosis(self):
        q = "SELECT usedDiagnosis FROM db_version"
        self.c.execute(q)
        res = self.c.fetchall()[0][0]
        if res == 1:
            r = True
        else:
            # has used diagnosis now; extremely bad coding style but I am tired
            q = "UPDATE db_version SET usedDiagnosis = 1"
            self.c.execute(q)
            self.conn.commit()
            r = False
        return r
    def saveLog(self, session_id, coords, diseaseName, district, time):
        q = "INSERT INTO local_disease_logs(disease_name, detected_time, detected_at, detected_by, detected_at_coords) VALUES ('{}', '{}', '{}', '{}', '{}')".format(diseaseName, datetime.datetime.strftime(time, "%m/%d/%Y, %H:%M:%S"), district, session_id, coords)
        self.c.execute(q)
        return self.conn.commit()
    def loadLogs(self, filter):
        q = "SELECT * FROM local_disease_logs"
        if filter == True:
            q = q+" WHERE uploaded = 0"
        self.c.execute(q)
        print(q)
        return self.c.fetchall()
    def clearPending(self):
        # q = "UPDATE local_disease_logs SET uploaded = 1"
        # self.c.execute(q)
        # return self.conn.commit()
        return  True