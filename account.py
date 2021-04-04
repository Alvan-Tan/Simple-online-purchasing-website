from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy.orm import sessionmaker
#json web token
import json
import jwt
import datetime
#from authenticate import token_required #The token verification script
from flask import Flask, request

#what should be our value?
SECRET_KEY = "secret"

flask_app = Flask(__name__)
CORS(flask_app)

flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/account'
flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(flask_app)

# Session = sessionmaker(bind = "innodb")
# session = Session()

# CORS(app)

class Account(db.Model):
    __tablename__ = 'account'

    AID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    phone = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    address = db.Column(db.String(64), nullable=False)

    def __init__(self, AID, name, password, phone, email, address):
        self.AID = AID
        self.name = name
        self.password = password
        self.phone = phone
        self.email = email
        self.address = address

    def json(self):
        return {"AID": self.AID, "name": self.name, "password": self.password, "phone": self.phone,  "email": self.email ,  "address": self.address}

#json web token
# @flask_app.route('/account', methods=['POST'])
# def loginFunction():
#     #retrieve from where?
#     email = request.form.get('email')
#     password = request.form.get('password')
#     #Generate token
#     timeLimit= datetime.datetime.utcnow() + datetime.timedelta(minutes=30) #set limit for user
#     payload = {"email": email,"exp":timeLimit}
#     token = jwt.encode(payload,SECRET_KEY)
#     return_data = {
#         "error": "0",
#         "message": "Successful",
#         "token": token.decode("UTF-8"),
#         "Elapse_time": f"{timeLimit}"
#         }
#     return flask_app.response_class(response=json.dumps(return_data), mimetype='application/json')

# #what is the anEndpoint? what is gonna be our Endpoint?
# @flask_app.route('/anEndpoint',methods=['POST'])
# @token_required #Verify token decorator
# def aWebService():
#     return_data = {
#         "error": "0",
#         "message": "You are verified"
#         }
#     return flask_app.response_class(response=json.dumps(return_data), mimetype='application/json')

#original code below

#Check if account exists, return confirmation if it exists, else return error
@flask_app.route("/login", methods=['POST'])
def login():
    
    data = request.get_json()
    email = data["email"]
    password = data["password"]

    account = Account.query.filter_by(email=email).first()
    if account:
        if password == account.password:
            timeLimit= datetime.datetime.utcnow() + datetime.timedelta(minutes=30) #set limit for user
            payload = {"email": email,"exp":timeLimit}
            token = jwt.encode(payload,SECRET_KEY)
            # return_data = {
            #     "error": "0",
            #     "message": "Successful",
            #     "token": token,
            #     "Elapse_time": f"{timeLimit}"
            #     }

            # return flask_app.response_class(response=json.dumps(return_data), mimetype='application/json'
            return jsonify(
                {
                    "code": 200,
                    "data": account.json(),
                    "message": "Account retrieved successfully",
                    "token": token,
                    #"return_data":return_data
                }
            )
        return jsonify(
        {
            "code": 401,
            "message": "Wrong password try again."
        }
        ), 401
    return jsonify(
        {
            "code": 404,
            "message": "Account not found."
        }
    ), 404


@flask_app.route("/verify", methods=['POST'])
def verify():

    data = request.get_json()
    token = data["token"]
    
    # authenticate stuff start
    try:
        # data = request.get_json()
        # token = data["token"]
        if token != '' and token != None:
            try:
                data = jwt.decode(token,SECRET_KEY, algorithms=['HS256'])
                return_data = {
                    "code": 201,
                    "message": "You Are verified"
                    }
                return flask_app.response_class(response=json.dumps(return_data), mimetype='application/json'),201
                
            except jwt.exceptions.ExpiredSignatureError:
                return_data = {
                    "code": 401,
                    "message": "Token has expired"
                    }
                return flask_app.response_class(response=json.dumps(return_data), mimetype='application/json'),401
            except:
                return_data = {
                    "code": 401,
                    "message": "Invalid Token"
                }
                return flask_app.response_class(response=json.dumps(return_data), mimetype='application/json'),401
        else:
            return_data = {
                "code" : 401,
                "message" : "Token required",
            }
            return flask_app.response_class(response=json.dumps(return_data), mimetype='application/json'),401
    except Exception as e:
        return_data = {
            "code" : 500,
            "message" : "An error occurred"
            }
        return flask_app.response_class(response=json.dumps(return_data), mimetype='application/json'),500
    # authenticate stuff end

@flask_app.route("/get_name/<string:email>", methods=["GET"])
def update_stock(email):
    person = Account.query.filter_by(email=email).first()
    if person:
        return jsonify(
            {
                "code": 200,
                "data": person.json(),
                "message": "Person found"
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Person not found."
        }
    ), 404

@flask_app.route("/get_email/<string:AID>", methods=["GET"])
def get_email_with_AID(AID):
    person = Account.query.filter_by(AID=AID).first()
    if person:
        return jsonify(
            {
                "code": 200,
                "data": person.json(),
                "message": "Person found",
                "email": person.email
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Person not found."
        }
    ), 404

if __name__ == "__main__":
    flask_app.run(port="5002", debug=True)