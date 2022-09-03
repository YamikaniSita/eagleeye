import sqlite3

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

