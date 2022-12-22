import json
from urllib import response
from flask import Flask, request, jsonify, make_response, render_template, redirect
from flask_marshmallow import Marshmallow
from models import db, Users, Disease, Symptom, Chemical, Control, ChangeLog, AppSessions, DiseaseLog, SMSClients
from schemas import ChemicalSchema, ControlSchema, SymptomSchema, UserSchema, DiseaseSchema, ChangeLogSchema, AppSessionsSchema, DiseaseLogSchema, SMSCLientsSchema
import hashlib
from sqlalchemy import or_
from changelog import ChangeLogManager
import datetime
from logs import DiseaseLogs
from alert import WarningSystem

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///eagleeye.db"
ms = Marshmallow(app)

db.init_app(app)
with app.app_context():
    db.create_all()
    

@app.route('/register', methods = ['POST'])
def registerUser():
    data = request.get_json(force=True)
    data['password'] = hashlib.md5(data['password'].encode()).hexdigest()
    success = False
    if not Users.query.filter_by(pNumber = data['pNumber']).first():
        user_schema = UserSchema()
        user = user_schema.load(data)
        db.session.add(user)
        db.session.commit()
        success = True
   
    return make_response(jsonify({"success": success}),200)

@app.route('/app/new-session', methods = ['POST'])
def startNewAppSession():
    data = request.get_json(force=True)
    app_session_schema = AppSessionsSchema()
    new_session = app_session_schema.load(data)
    db.session.add(new_session)
    db.session.commit()
    session_id = new_session.id

    return make_response(jsonify({'success': True, 'session_id': session_id}))

@app.route('/profile/<pNumber>')
def getUserProfile(pNumber):
    profile = None
    user = UserSchema(many=True).dump(Users.query.filter_by(pNumber = pNumber))
    if(user):
        profile = user
    return make_response(jsonify({'profile':profile}))
    
@app.route('/app/user-list/', methods=['GET'])
def loadUsers():
    get_users = Users.query.filter(Users.role != 'app_user')
    user_schema = UserSchema(many=True)
    users = user_schema.dump(get_users)
    return make_response(jsonify({'users': users}))

@app.route('/app/', methods=['GET'])
def render_login():
    return render_template('login_page.html')

@app.route('/app/login/', methods =['POST'])
def auth_admin():
    data = request.get_json(force=True)
    current_user = Users.query.filter_by(name = data['userName']).first()
    resp = make_response(jsonify({'success': False}))
    if current_user:
        if hashlib.md5(data['userPassword'].encode()).hexdigest() == current_user.password:  
            if current_user.role != 'app_user':
                resp = make_response(jsonify({'success': True}))
                resp.set_cookie('user', current_user.name, max_age=60*60*24)
    return resp

@app.route('/app/panel/')
def render_panel():
    if request.cookies.get('user'):
        user_ = request.cookies.get('user')
        user_details = Users.query.filter_by(name = user_).first()
        return render_template('admin_home_main.html', user_details = user_details)
    else:
        #loggin
        return redirect('/app/', code=302)

@app.route('/app/add-disease', methods=['POST'])
def add_disease():
    data = request.get_json(force = True)
    log_schema = ChangeLogSchema()
    new_log = log_schema.load(ChangeLogManager().to_change_log_object(type='new_disease', data_object=data))
    db.session.add(new_log)
    db.session.commit()
    # change log committed early to prevent log failure
    disease_schema = DiseaseSchema()
    disease = disease_schema.load(data)
    db.session.add(disease)
    db.session.commit()
    id = disease.id
    return make_response(jsonify({"success": True, "id":id}), 200)

@app.route('/app/get-diseases/')
def get_diseases():
    get_diseases = Disease.query.filter(Disease.name != 'Healthy')
    disease_schema = DiseaseSchema(many = True)
    diseases = disease_schema.dump(get_diseases)
    return make_response(jsonify({"diseases":diseases}))

@app.route('/app/fetch_disease', methods = ['POST'])
def fetch_disease():
    disease_id = request.get_json(force = True)['id']
    general_info = DiseaseSchema(many = True).dump(Disease.query.filter_by(id = disease_id))
    symptoms = SymptomSchema(many=True).dump(Symptom.query.filter_by(disease_id = disease_id))
    controls = ControlSchema(many = True).dump(Control.query.filter_by(disease_id = disease_id))
    chemicals = ChemicalSchema(many = True).dump(Chemical.query.filter_by(disease_id = disease_id))

    return make_response(jsonify({"general_information":general_info, "symptoms": symptoms, "controls": controls, "chemicals": chemicals}))

@app.route('/app/add-symptom', methods = ['POST'])
def add_symptom():
    req_data = request.get_json(force = True)
    disease_ = Disease.query.filter_by(id = req_data['disease_id']).first()
    disease_ = disease_.name
    log_schema = ChangeLogSchema()
    new_log = log_schema.load(ChangeLogManager().to_change_log_object(type='new_symptom', data_object={"disease_key":disease_, "name":req_data['name']}))
    db.session.add(new_log)
    db.session.commit()
    symptom = SymptomSchema().load(req_data)
    db.session.add(symptom)
    db.session.commit()
    return make_response(jsonify({"lastElement":symptom.id}))

@app.route('/app/add-control', methods = ['POST'])
def add_control():
    req_data = request.get_json(force = True)
    disease_ = Disease.query.filter_by(id = req_data['disease_id']).first()
    disease_ = disease_.name
    log_schema = ChangeLogSchema()
    new_log = log_schema.load(ChangeLogManager().to_change_log_object(type='new_control', data_object={"disease_key":disease_, "control":req_data['control']}))
    db.session.add(new_log)
    db.session.commit()
    control = ControlSchema().load(req_data)
    db.session.add(control)
    db.session.commit()
    return make_response(jsonify({"lastElement":control.id}))

@app.route('/app/add-chemical', methods = ['POST'])
def add_chemical():
    req_data = request.get_json(force = True)
    chemical = ChemicalSchema().load(req_data)
    db.session.add(chemical)
    db.session.commit()
    disease_ = Disease.query.filter_by(id = req_data['disease_id']).first()
    disease_ = disease_.name
    log_schema = ChangeLogSchema()
    new_log = log_schema.load(ChangeLogManager().to_change_log_object(type='new_chemical', data_object={"disease_key":disease_, "chemical_name":req_data['chemical_name'], "dosage":req_data['dosage']}))
    db.session.add(new_log)
    db.session.commit()
    return make_response(jsonify({"lastElement":chemical.id}))

@app.route('/app/reports/brief/')
def generate_brief_report():
    app_users = Users.query.filter(Users.role == 'app_user').count()
    experts = Users.query.filter(Users.role == 'expert').count()
    admins = Users.query.filter(Users.role == 'admin').count() + 1#admin core is default 1
    total_diagnosis = len(DiseaseLog.query.all())
    positive_cases = DiseaseLog.query.filter(DiseaseLog.disease_detected != 7).count() #Healthy
    sms_warnings = DiseaseLog.query.filter(DiseaseLog.triggered_sms == 1).count()
    sms_clients = len(SMSClients.query.all())
    return make_response(jsonify({"admins":admins, "experts":experts, "app_users":app_users, "sms_clients":sms_clients, "diagnosis":total_diagnosis, "positives":positive_cases, "sms_warnings":sms_warnings}))

@app.route('/app/changelog/get', methods=['POST'])
def generate_changelog():
    app_last_update = datetime.datetime.strptime(request.get_json(force = True)['app_last_update'], "%m/%d/%Y, %H:%M:%S")
    app_last_update = app_last_update - datetime.timedelta(hours = 2, minutes=0) #GMT+2 to GMT
    log = ChangeLogSchema(many=True).dump(ChangeLog.query.filter(ChangeLog.time > app_last_update))
    return make_response(jsonify({'change_log':log}))

@app.route('/logs/add', methods = ['POST'])
def addToLog():
    data = request.get_json(force = True)
    print(data)
    for i in data['logs']:
        diseaseName = i[1]
        detected_at = i[2]
        detected_by = i[3]
        detected_at_coords = i[5]
        # detection_time = datetime.datetime.strptime(i[6], "%m/%d/%Y, %H:%M:%S")

        detection_time = i[6]
        log_entry = DiseaseLogs().toDiseaseLog(diseaseName, detected_by, detected_at, detected_at_coords, detection_time)
        trigger_ = WarningSystem().isAlertRequired(log_entry)
        if trigger_:
          WarningSystem().warn(log_entry)
        #   log_entry['triggered_sms'] = 1
        log_entry = DiseaseLogSchema().load(log_entry)
        db.session.add(log_entry)
        db.session.commit()

    return make_response(jsonify({'success':True}))

@app.route('/app/sms/add_client', methods = ['POST'])
def addClient():
    data = request.get_json(force=True)
    sms_schema = SMSCLientsSchema()
    client = sms_schema.load(data)
    db.session.add(client)
    db.session.commit()
    return make_response(jsonify({'success':True}))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)