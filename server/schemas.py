from sqlite3 import sqlite_version
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models import ChangeLog, db, Users, Disease, Control, Chemical, Symptom
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

class DiseaseSchema(SQLAlchemyAutoSchema):
    class Meta(SQLAlchemyAutoSchema.Meta):
        model = Disease
        sqlite_session = db.session
        load_instance = True
    id = fields.Number(dump_only=True)
    name = fields.String(required=True)
    desc = fields.String(required=True)

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
