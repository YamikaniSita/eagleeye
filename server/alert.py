from models import AppSessions, Disease, Control, Chemical, Symptom
from schemas import AppSessionsSchema, DiseaseSchema, ControlSchema, ChemicalSchema, SymptomSchema

class WarningSystem:
    def isAlertRequired(self, diseaseLog):
        return True
    def warn(self, diseaseLog):
        print(diseaseLog)
        disease = DiseaseSchema().dump(Disease.query.get(diseaseLog['disease_detected']))
        diseaseName = disease['name']
        symptoms = SymptomSchema(many = True).dump(Symptom.query.filter(Symptom.disease_id == diseaseLog['disease_detected']))
        controls = ControlSchema(many = True).dump(Control.query.filter(Control.disease_id == diseaseLog['disease_detected']))
        chemicals = ChemicalSchema(many = True).dump(Chemical.query.filter(Control.disease_id == diseaseLog['disease_detected']))
        recepients = AppSessionsSchema(many = True).dump(AppSessions.query.filter(AppSessions.district == diseaseLog['detection_locale'], AppSessions.id != diseaseLog['detected_by']))
        s_list = ""
        c_list = ""
        ch_list = ""
        for i in symptoms:
            s_list += ", "+i['name']
        for i in controls:
            c_list += ", "+i['control']
        for i in chemicals:
            ch_list += ", "+i['chemical_name']
        message = "A case of {} was detected in your area. The condition can be noticed by{}. Controls include{}. Following chemicals can be applied if symptoms noticed{}. Thank you".format(diseaseName, s_list, c_list, ch_list)
        print(recepients)