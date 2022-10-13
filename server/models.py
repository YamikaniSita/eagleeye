from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.sql import func
db = SQLAlchemy()

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    district = db.Column(db.String(30))
    pNumber = db.Column(db.String(10))
    password = db.Column(db.String(100))
    role = db.Column(db.String(30))

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self
    def __init__(self, name, district, password, pNumber, role):
        self.name = name
        self.district = district
        self.password = password
        self.pNumber = pNumber
        self.role = role
    def __repr__(self):
        return '<User %d>' % self.id

class Disease(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    desc = db.Column(db.String(500))
    symptoms = db.relationship("Symptom", backref='disease', cascade = 'all, delete-orphan', lazy = True)
    controls = db.relationship("Control", backref='disease', cascade = 'all, delete-orphan', lazy = True)
    chemicals = db.relationship("Chemical", backref='disease', cascade = 'all, delete-orphan', lazy = True)

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, name, desc):
        self.name = name
        self.desc = desc

    def __repr__(self):
        return '<Disease %d>' % self.id

class Symptom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    disease_id = db.Column(db.Integer, ForeignKey("disease.id"))

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self
    
    def __init__(self, name, disease_id):
        self.name = name
        self.disease_id = disease_id

    def __repr__(self):
        return '<Symptom %d>' % self.id
    
class Control(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    control = db.Column(db.String(1000))
    disease_id = db.Column(db.Integer, ForeignKey("disease.id"))

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self
    
    def __init__(self, control, disease_id):
        self.control = control
        self.disease_id = disease_id

    def __repr__(self):
        return '<Control %d>' % self.id

class Chemical(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chemical_name = db.Column(db.String(1000))
    dosage = db.Column(db.String(1000))
    disease_id = db.Column(db.Integer, ForeignKey("disease.id"))

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self
    
    def __init__(self, chemical_name, dosage, disease_id):
        self.chemical_name = chemical_name
        self.disease_id = disease_id
        self.dosage = dosage

    def __repr__(self):
        return '<Chemical %d>' % self.id

class ChangeLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(1000))
    values = db.Column(db.JSON)
    time = db.Column(db.DateTime, server_default=func.now())

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self
    
    def __init__(self, type, values):
        self.type = type
        self.values = values

    def __repr__(self):
        return '<LogNumber %d>' % self.id

    


    

