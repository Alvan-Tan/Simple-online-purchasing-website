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

@app.route("/preorder/restock")
def preorder_restock():
    #get name and qty of new stock
    data = request.get_json()
    product_name = data["product_name"]
    new_stock = data["new_stock"]

    #filter out preorders by name of new stock
    preorder = Preorder.query.filter_by(product_name=product_name)
    #holder for later
    preorder_list = []
    count = 0
    if preorder:
        for i in preorder:
            #run until new_stock runs out, 
            #if new_stock greater than PO , remainder can send to normal stock
            #if new_stock lesser than PO, 0 to send to stocks, newest PO will be unfulfilled
            quantity = i.quantity
            new_stock = int(new_stock)
            if new_stock != 0:
                if new_stock >= quantity:
                    preorder_list.append(i.json())
                    db.session.delete(i)
                    db.session.commit()
                    #drop new_stock 1 by 1
                    new_stock -= quantity
                    count += quantity
                else:
                    quantity -= new_stock
                    count += new_stock
                    new_stock = 0
                    i.quantity = quantity
                    preorder_list.append(i.json())
                    db.session.commit()
                    break
                
        return jsonify(
            {
                "code": 200,
                "data": {
                    "product_name":product_name,
                    "preorders" : preorder_list,
                    "new_stock" : new_stock
                },
                "message": str(count) + " preorder(s) cleared."
            }
        )

    return jsonify(
        {
            "code": 404,
            "message": "There are no Preorder Records."
        }
    ), 404






if __name__ == "__main__":
    app.run(port="5005", debug=True)