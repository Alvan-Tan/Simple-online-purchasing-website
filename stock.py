from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy.orm import sessionmaker


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/stock'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Session = sessionmaker(bind = "innodb")
# session = Session()

# CORS(app)

class Stock(db.Model):
    __tablename__ = 'stock'

    SID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    availableforPO = db.Column(db.Boolean)

    def __init__(self, SID, name, quantity, availableforPO):
        self.SID = SID
        self.name = name
        self.quantity = quantity
        self.availableforPO = availableforPO

    def json(self):
        return {"SID": self.SID, "name": self.name, "quantity": self.quantity, "availableforPO": self.availableforPO}

#Return stocklist, not sure whats the usage yet.
@app.route("/stock")
def return_all_stock():
    stocklist = Stock.query.all()
    if len(stocklist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "stocks": [stock.json() for stock in stocklist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no stocks."
        }
    ), 404

#Check if stock exist, minus 1 and return confirmation if it exist, else return error
@app.route("/stock/<string:name>", methods=["PUT"])
def update_stock(name):
    stock = Stock.query.filter_by(name=name).first()
    if stock:
        quantity = request.get_json()
        stock.quantity -= quantity["quantity"]
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": stock.json(),
                "message": "stock deducted successfully"
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Stock not found."
        }
    ), 404


if __name__ == "__main__":
    app.run(port="5001", debug=True)