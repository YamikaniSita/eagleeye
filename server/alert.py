from models import AppSessions, Disease, Control, Chemical, Symptom
from schemas import AppSessionsSchema, DiseaseSchema, ControlSchema, ChemicalSchema, SymptomSchema, SMSClients, SMSCLientsSchema

class WarningSystem:
    def isAlertRequired(self, diseaseLog):
        if diseaseLog['disease_detected'] == 7:
            # healthy
            return False
        return True
    def warn(self, diseaseLog):
        print(diseaseLog)
        disease = DiseaseSchema().dump(Disease.query.get(diseaseLog['disease_detected']))
        diseaseName = disease['name']
        symptoms = SymptomSchema(many = True).dump(Symptom.query.filter(Symptom.disease_id == diseaseLog['disease_detected']))
        controls = ControlSchema(many = True).dump(Control.query.filter(Control.disease_id == diseaseLog['disease_detected']))
        recepients = SMSCLientsSchema(many = True).dump(SMSClients.query.with_entities(SMSClients.phoneNumber).filter(SMSClients.district == diseaseLog['detection_locale']))
        s_list = ""
        c_list = ""
        for i in symptoms:
            s_list += ", "+i['name']
        for i in controls:
            c_list += ", "+i['control']
        message = "A case of {} was detected near you. It can be noticed by {}. Controls include{}.".format(diseaseName, s_list, c_list)
        return (recepients, message)