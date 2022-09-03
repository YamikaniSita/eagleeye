import json
from urllib import response
from flask import Flask, request, jsonify, make_response
from flask_marshmallow import Marshmallow
from models import db, Users
from schemas import UserSchema
import hashlib

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

@app.route('/login', methods = ['POST'])
def login():
    data = request.get_json(force=True)
    success = False
    current_user = Users.query.filter_by(pNumber = data['pNumber']).first()
    if current_user:
        if hashlib.md5(data['password'].encode()).hexdigest() == current_user.password:
            success = True

    return make_response(jsonify({'success': success}))

@app.route('/profile/<pNumber>')
def getUserProfile(pNumber):
    profile = None
    user = UserSchema(many=True).dump(Users.query.filter_by(pNumber = pNumber))
    if(user):
        profile = user
    return make_response(jsonify({'profile':profile}))
    
@app.route('/', methods=['GET'])
def loadUsers():
    get_users = Users.query.all()
    print('/')
    author_schema = UserSchema(many=True)
    users = author_schema.dump(get_users)
    return make_response(jsonify({'users': users}))


if __name__ == '__main__':
    app.run(debug=True)