from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy.orm import sessionmaker
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/preorder'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app)

class Preorder(db.Model):
    __tablename__ = 'preorder'

    POID = db.Column(db.Integer, primary_key=True)
    AID = db.Column(db.Integer, nullable=False)
    product_name = db.Column(db.String(64), nullable=False)
    quantity = db.Column(db.Integer,  nullable=False)
    payment_status = db.Column(db.String(64), nullable=False)
    total_price = db.Column(db.Integer,  nullable=False)
    address = db.Column(db.String(64), nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)


    def json(self):
        return {"POID": self.POID, "AID": self.AID, "product_name": self.product_name, "quantity" :self.quantity, "payment_status": self.payment_status, "total_price":self.total_price, "address": self.address, "datetime": self.datetime}

@app.route("/preorder")
def return_all_preorder():
    preorderrecord = Preorder.query.all()
    if len(preorderrecord):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "stocks": [record.json() for record in preorderrecord]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no Preorder Records."
        }
    ), 404

#Create a shipping record and return success or failure
@app.route("/preorder/create_record", methods=["POST"])
def create_preorder_record():

    data = request.get_json()
    data["datetime"] = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    record = Preorder(**data)

    try:
        db.session.add(record)
        db.session.commit()

    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while creating the preorder. " + str(e)
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": record.json()
        }
    ), 201





if __name__ == "__main__":
    app.run(port="5005", debug=True)