from models import Disease
from schemas import DiseaseSchema
class DiseaseLogs:
    def toDiseaseLog(self, diseaseName, detectedBy, detection_locale, detection_coords, time):
        disease = DiseaseSchema(many=True).dump(Disease.query.filter(Disease.name == diseaseName))[0]['id']
        print(disease)
        dict_ = {
            'disease_detected':disease,
            'detection_locale':detection_locale,
            'detected_coords':detection_coords,
            'detected_by':detectedBy,
            'time': time
        }
        return dict_