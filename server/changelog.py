import json
class ChangeLogManager():
    def to_change_log_object(self, type, data_object):
        dict_ = {}
        if type == 'new_disease':
            dict_ = {
                "type": "new_disease",
                "values" : {
                    "name":data_object['name'],
                    "desc":data_object['desc']
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
        return dict_
