import json
class ChangeLogManager():
    def to_change_log_object(self, type, data_object):
        dict_ = {}
        if type == 'new_disease':
            dict_ = {
                "type": "new_disease",
                "values" : {
                    "name":data_object['name'],
                    "desc":data_object['desc'],
                    "name_ch":data_object['name_ch'],
                    "desc_ch":data_object['desc_ch'],
                    "langs": data_object['langs']
                }
            }
            return dict_
        elif type == 'new_symptom':
            dict_ = {
                "type": "new_symptom",
                "values": {
                    "name": data_object['name'],
                    "disease_key": data_object['disease_key']
                }
            }
        elif type == 'new_control':
            dict_ = {
                "type": "new_control",
                "values": {
                    "control": data_object['control'],
                    "disease_key": data_object['disease_key']
                }
            }
        elif type == 'new_chemical':
            dict_ = {
                "type":"new_chemical",
                "values": {
                    "chemical_name": data_object['chemical_name'],
                    "dosage": data_object['dosage'],
                    "disease_key": data_object['disease_key']
                }
            }
        return dict_
