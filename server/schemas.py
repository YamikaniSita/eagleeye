from sqlite3 import sqlite_version
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models import ChangeLog, ControlCH, SymptomCH, db, Users, Disease, Control, Chemical, Symptom, AppSessions, DiseaseLog, SMSClients
from marshmallow import fields


class UserSchema(SQLAlchemyAutoSchema):
    class Meta(SQLAlchemyAutoSchema.Meta):
        model = Users
        sqlite_session = db.session
        load_instance = True
    id = fields.Number(dump_only=True)
    name = fields.String(required=True)
    password = fields.String(required=True)
    district = fields.String(required=True)
    pNumber = fields.String(required=True)
    role = fields.String(required=True)

class AppSessionsSchema(SQLAlchemyAutoSchema):
    class Meta(SQLAlchemyAutoSchema.Meta):
        model = AppSessions
        sqlite_session = db.session
        load_instance = True
    id = fields.Number(dump_only = True)
    district = fields.String(required = True)

class SMSCLientsSchema(SQLAlchemyAutoSchema):
    class Meta(SQLAlchemyAutoSchema.Meta):
        model = SMSClients
        sqlite_session = db.session
        load_instance = True
    id = fields.Number(dump_only = True)
    name = fields.String(required = True)
    district = fields.String(required=True)
    phoneNumber = fields.String(required = True)
    
class DiseaseSchema(SQLAlchemyAutoSchema):
    class Meta(SQLAlchemyAutoSchema.Meta):
        model = Disease
        sqlite_session = db.session
        load_instance = True
    id = fields.Number(dump_only=True)
    name = fields.String(required=True)
    desc = fields.String(required=True)
    name_ch = fields.String(required=False)
    desc_ch = fields.String(required=False)
    langs = fields.String(required=False)

class SymptomSchema(SQLAlchemyAutoSchema):
    class Meta(SQLAlchemyAutoSchema.Meta):
        model = Symptom
        sqlite_session = db.session
        load_instance = True
    id = fields.Number(dump_only=True)
    name = fields.String(required=True)
    disease_id = fields.Number(required=True)

class ControlSchema(SQLAlchemyAutoSchema):
    class Meta(SQLAlchemyAutoSchema.Meta):
        model = Control
        sqlite_session = db.session
        load_instance = True
    id = fields.Number(dump_only=True)
    control = fields.String(required=True)
    disease_id = fields.Number(required=True)

class SymptomSchemaCH(SQLAlchemyAutoSchema):
    class Meta(SQLAlchemyAutoSchema.Meta):
        model = SymptomCH
        sqlite_session = db.session
        load_instance = True
    id = fields.Number(dump_only=True)
    name = fields.String(required=True)
    disease_id = fields.Number(required=True)

class ControlSchemaCH(SQLAlchemyAutoSchema):
    class Meta(SQLAlchemyAutoSchema.Meta):
        model = ControlCH
        sqlite_session = db.session
        load_instance = True
    id = fields.Number(dump_only=True)
    control = fields.String(required=True)
    disease_id = fields.Number(required=True)

class ChemicalSchema(SQLAlchemyAutoSchema):
    class Meta(SQLAlchemyAutoSchema.Meta):
        model = Chemical
        sqlite_session = db.session
        load_instance = True
    id = fields.Number(dump_only = True)
    chemical_name = fields.String(required=True)
    dosage = fields.String(required = False)
    disease_id = fields.Number(required = True)

class ChangeLogSchema(SQLAlchemyAutoSchema):
    class Meta(SQLAlchemyAutoSchema.Meta):
        model = ChangeLog
        sqlite_version = db.session
        load_instance = True
    id = fields.Number(dump_only = True)
    type = fields.String(required = True)
    values = fields.Dict(required = True)
    time = fields.DateTime(dump_only = True)

class DiseaseLogSchema(SQLAlchemyAutoSchema):
    class Meta(SQLAlchemyAutoSchema.Meta):
        model = DiseaseLog
        sqlite_version = db.session
        load_instance = True
    id = fields.Number(dump_only = True)
    detection_locale = fields.String(required = True)
    detected_coords = fields.String(required = True)
    triggered_sms = fields.Integer(required = True)
    detected_by = fields.Integer(required = True)
    disease_detected = fields.Integer(required = True)
    time = fields.String(required = True)