from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from flask_sqlalchemy import SQLAlchemy
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

