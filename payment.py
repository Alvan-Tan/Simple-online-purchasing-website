from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy.orm import sessionmaker


app = Flask(__name__)


CORS(app)

#Connect to paypal api to process payment
@app.route("/payment")
def paypal():
    #if successful, return success code with payment completed details
    if True:
        # return jsonify(
        #     {
        #         "code": 200,
        #         "data": {
        #             "stocks": [stock.json() for stock in stocklist]
        #         }
        #     }
        # )
    #if unsuccessful, return error code and cancel order
    return jsonify(
        {
            "code": 404,
            "message": "Payment not successful"
        }
    ), 404


if __name__ == "__main__":
    app.run(port="5002", debug=True)