from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models import db, Users
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
    