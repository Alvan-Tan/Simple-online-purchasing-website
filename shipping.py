from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy.orm import sessionmaker


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/shipping'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# CORS(app)

class Shipping(db.Model):
    __tablename__ = 'shipping'

    SPID = db.Column(db.Integer, primary_key=True)
    AID = db.Column(db.Integer, nullable=False)
    OID = db.Column(db.Integer, nullable=False)
    product_name = db.Column(db.String(64), nullable=False)
    payment_status = db.Column(db.String(64), nullable=False)
    address = db.Column(db.String(64), nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)

    # def __init__(self, SPID, AID, OID, PID, paymentstatus, shippingdetails, datetime):
    #     self.SPID = SPID
    #     self.AID = AID
    #     self.OID = OID
    #     self.PID = PID
    #     self.paymentstatus = paymentstatus
    #     self.shippingdetails = shippingdetails
    #     self.datetime = datetime

    def json(self):
        return {"SPID": self.SPID, "AID": self.AID, "OID": self.OID, "product_name": self.product_name, "payment_status": self.payment_status, "address": self.address, "datetime": self.datetime}

#Return shipping list, not sure whats the usage yet.
@app.route("/shipping")
def return_shipping_record():
    shippingrecord = Shipping.query.all()
    if len(shippingrecord):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "stocks": [record.json() for record in shippingrecord]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no Shipping Records."
        }
    ), 404

#Create a shipping record and return success or failure
@app.route("/shipping/create_record", methods=["POST"])
def create_shipping_record():
    
    # if (Shipping.query.filter_by(SPID=SPID).first()):
    #     return jsonify(
    #         {
    #             "code": 400,
    #             "data": {
    #                 "SPID": SPID
    #             },
    #             "message": "Shipping record already exists."
    #         }
    #     ), 400

    data = request.get_json()
    record = Shipping(**data)

    try:
        db.session.add(record)
        db.session.commit()

    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while creating the order. " + str(e)
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": record.json()
        }
    ), 201





if __name__ == "__main__":
    app.run(port="5003", debug=True)