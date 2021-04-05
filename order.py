from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy.orm import sessionmaker
from os import environ


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/order'
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://root@localhost:3306/order'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# CORS(app)

class Order(db.Model):
    __tablename__ = 'order'

    OID = db.Column(db.Integer, primary_key=True)
    AID = db.Column(db.Integer, nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)
    payment_status = db.Column(db.String(64), nullable=False)
    product_name = db.Column(db.String(64), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(64), nullable=False)
    
    # def __init__(self, SPID, AID, OID, PID, paymentstatus, shippingdetails, datetime):
    #     self.SPID = SPID
    #     self.AID = AID
    #     self.OID = OID
    #     self.PID = PID
    #     self.paymentstatus = paymentstatus
    #     self.shippingdetails = shippingdetails
    #     self.datetime = datetime

    def json(self):
        return {"OID": self.OID, "AID": self.AID, "datetime": self.datetime, "payment_status": self.payment_status, "product_name": self.product_name, "quantity" : self.quantity, "total_price": self.total_price, "datetime": self.datetime}

#Return shipping list, not sure whats the usage yet.
@app.route("/order")
def return_order_record():
    orderrecord = Order.query.all()
    if len(orderrecord):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "stocks": [record.json() for record in orderrecord]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no Order Records."
        }
    ), 404

#Create a shipping record and return success or failure
@app.route("/order/create_record", methods=["POST"])
def create_order_record():
    
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
    record = Order(**data)

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
    app.run(host="0.0.0.0", port=5004, debug=True)