from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy.orm import sessionmaker


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/account'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Session = sessionmaker(bind = "innodb")
# session = Session()

# CORS(app)

class Stock(db.Model):
    __tablename__ = 'account'

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
@app.route("/account_check")
def return_account_validity():
    # stocklist = Stock.query.all()
    # if len(stocklist):
    #     return jsonify(
    #         {
    #             "code": 200,
    #             "data": {
    #                 "stocks": [stock.json() for stock in stocklist]
    #             }
    #         }
    #     )
    if True:
         return jsonify(
            {
                "code": 200,
                "message": "Valid User"
            }
        )
    else:
        return jsonify(
            {
                "code": 404,
                "message": "Invalid User"
            }
        ), 404

if __name__ == "__main__":
    app.run(port="5002", debug=True)