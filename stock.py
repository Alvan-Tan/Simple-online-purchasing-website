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

CORS(app)

class Stock(db.Model):
    __tablename__ = 'stock'

    SID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    pictureURL = db.Column(db.String(64), nullable=False)

    # def __init__(self, SID, name, quantity, availableforPO):
    #     self.SID = SID
    #     self.name = name
    #     self.quantity = quantity
    #     self.availableforPO = availableforPO


    def json(self):
        return {"SID": self.SID, "name": self.name, "price": self.price, "quantity": self.quantity, "pictureURL": self.pictureURL}

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
@app.route("/stock/minus/<string:name>", methods=["PUT"])
def minus_stock(name):
    stock = Stock.query.filter_by(name=name).first()
    quantity = request.get_json() 
    if stock:
        if stock.quantity >= int(quantity["quantity"]):
            stock.quantity -= int(quantity["quantity"])
            db.session.commit()
            return jsonify(
                {
                    "code": 200,
                    "data": stock.json(),
                    "message": "stock deducted successfully"
                }
            )
        else:
            return jsonify(
                {
                    "code": 404,
                    "data": stock.json(),
                    "message": "Out of stocks",
                }
            ), 404

    return jsonify(
        {
            "code": 404,
            "message": "Stock not found."
        }
    ), 404

@app.route("/stock/add/<string:name>", methods=["PUT"])
def add_stock(name):
    stock = Stock.query.filter_by(name=name).first()
    quantity = request.get_json() 
    if stock:
        stock.quantity += int(quantity["quantity"])
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": stock.json(),
                "message": "stock added successfully"
            }
        )

    return jsonify(
        {
            "code": 404,
            "message": "Stock not found."
        }
    ), 404

@app.route("/stock/<string:name>")
def find_by_sname(name):
    stock = Stock.query.filter_by(name=name).first()
    if stock:
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": stock.json(),
                "message": "Stock found."
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "No such shoe name available."
        }
    ), 404

@app.route("/addNewShoe/<string:name>", methods=["POST"])
def create_shoe(name):
    if(Stock.query.filter_by(name=name).first()):
        return jsonify(
            {
                "code": 400,
                "message": "Shoe Name already exists."
            }
        ), 400

    data = request.get_json()
    stock = Stock(**data)

    try:
        db.session.add(stock)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "name": name
                },
                "message": "An error occurred creating the shoe."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": stock.json()
        }
    ), 201


if __name__ == "__main__":
    app.run(port="5001", debug=True)