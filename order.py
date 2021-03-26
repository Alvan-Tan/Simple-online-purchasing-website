#!/usr/bin/env python3
# The above shebang (#!) operator tells Unix-like environments
# to run this file as a python3 script

import json
import os

import amqp_setup

monitorBindingKey='*.order'

#start of my code#

from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS 
from sqlalchemy.orm import sessionmaker


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/order'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Order(db.Model):
    __tablename__ = 'order'

    OID = db.Column(db.Integer, primary_key=True)
    AID = db.Column(db.Integer, nullable=False)
    product_name = db.Column(db.String(64), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Integer, nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)
    payment_status = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String(64), nullable=False)

    def json(self):
        return {"OID": self.OID, "AID": self.AID, "product_name": self.product_name, "quantity": self.quantity, "total_price": self.total_price, "datetime": self.datetime, "payment_status": self.payment_status, "address": self.address}

#end of my code#

def receiveOrder():
    amqp_setup.check_setup()
    
    queue_name = "Order"  

    # set up a consumer and start to wait for coming messages
    amqp_setup.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    amqp_setup.channel.start_consuming() # an implicit loop waiting to receive messages; 
    #it doesn't exit by default. Use Ctrl+C in the command window to terminate it.

def callback(channel, method, properties, body): # required signature for the callback; no return
    print("\nReceived an order by " + __file__)
    processOrder(body)
    print() # print a new line feed

def processOrder(orderDetails):
    print("Printing the order message:")
    try:
        # Lay Foo - the following line converts orderDetails (json text) to a python dictionary
        order = json.loads(orderDetails)
        print("--JSON:", order)

        #start of my code#
        # Lay Foo - replace
        # Was: error_record = Error(1, error)
        # To: 
        order_record = Order(AID=order["AID"], product_name=order["product_name"], quantity=order["quantity"], total_price=order["total_price"], datetime=order["datetime"], payment_status=order["payment_status"], address=order["address"])

        db.session.add(order_record)
        db.session.commit()
        #end of my code#
    except Exception as e:
        print("Exception:", e)
        print("--DATA:", orderDetails)
    print()


if __name__ == "__main__":  # execute this program only if it is run as a script (not by 'import')    
    print("\nThis is " + os.path.basename(__file__), end='')
    print(": monitoring routing key '{}' in exchange '{}' ...".format(monitorBindingKey, amqp_setup.exchangename))
    receiveOrder()
