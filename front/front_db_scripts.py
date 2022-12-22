import sqlite3
import datetime
from kivymd.uix.snackbar import Snackbar


class DBHandler:
    conn = sqlite3.connect('frontdb.db')
    c = conn.cursor()
    def getDiseaseList(self, user_lang):
        records = []
        if user_lang == 'ch':
            self.c.execute("SELECT _id, name_ch FROM diseases WHERE name != 'Healthy' AND langs = 'eng,ch'")
            records = self.c.fetchall()
            self.c.execute("SELECT _id, name FROM diseases WHERE name != 'Healthy' AND langs = 'eng'")
            b = self.c.fetchall()
            if len(b) > 0:
                # some diseases not translated yet
                Snackbar(text="Matenda ena sanamasulilidwe mu Chichewa.").open()
                records = self.append_results(records, b)
        elif user_lang == 'eng':
            self.c.execute("SELECT _id, name FROM diseases WHERE name != 'Healthy'")
            records = self.c.fetchall()
        print(records)
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
    def addDisease(self, name, desc, name_ch, desc_ch, langs):
        self.c.execute("INSERT INTO diseases (name, desc, name_ch, desc_ch, langs) VALUES ('{}', '{}', '{}', '{}', '{}')".format(name, desc, name_ch, desc_ch, langs))
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
    def saveLog(self, session_id, coords, diseaseLabel, district, time):
        q = "SELECT name,_id FROM diseases"
        self.c.execute(q)
        res = self.c.fetchall()
        min = {'disease': res[0][0], 'id':res[0][1], 'distance': self.lev_distance(diseaseLabel, res[0][0])}
        for i in range(1, len(res)):
            distance = self.lev_distance(diseaseLabel, res[i][0])
            if distance < min["distance"]:
                min["disease"] = res[i][0]
                min["distance"] = distance
                min["id"] = res[i][1]
        diseaseName = min["disease"]
        q = "INSERT INTO local_disease_logs(disease_name, detected_time, detected_at, detected_by, detected_at_coords) VALUES ('{}', '{}', '{}', '{}', '{}')".format(diseaseName, datetime.datetime.strftime(time, "%m/%d/%Y, %H:%M:%S"), district, session_id, coords)
        self.c.execute(q)
        return min
    def loadLogs(self, filter):
        q = "SELECT * FROM local_disease_logs"
        if filter == True:
            q = q+" WHERE uploaded = 0"
        self.c.execute(q)
        print(q)
        return self.c.fetchall()
    def clearPending(self):
        print('clear_pointP2')
        q = "UPDATE local_disease_logs SET uploaded = 1"
        self.c.execute(q)
        return self.conn.commit()
    
        # db utility functions
    def lev_distance(self, a, b):
        #to reader: This is just a way to get this to work..its overkill I know.
        matrix = [[0 for i in range(len(b) + 1)] for j in range(len(a) + 1)]
        for i in range(len(a) + 1):
            matrix[i][0] = i
        for j in range(len(b) + 1):
            matrix[0][j] = j
        for i in range(1, len(a) + 1):
            for j in range(1, len(b) + 1):
                if a[i-1] == b[j-1]:
                    matrix[i][j] = matrix[i - 1][j - 1]
                else:
                    matrix[i][j] = min(
                        matrix[i - 1][j] + 1,
                        matrix[i][j - 1] + 1,
                        matrix[i - 1][j - 1] + 1
                )
        return matrix[len(a)][len(b)]
    
    def append_results(self, a, b):
        c = []
        for i in a:
            c.append(i)
        for i in b:
            c.append(i)
        return c