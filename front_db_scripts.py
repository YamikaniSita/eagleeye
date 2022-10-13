import sqlite3
import datetime

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