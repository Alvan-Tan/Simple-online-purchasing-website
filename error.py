#!/usr/bin/env python3
# The above shebang (#!) operator tells Unix-like environments
# to run this file as a python3 script

import json
import os
from os import environ
import amqp_setup

monitorBindingKey='*.error'

#start of my code#

from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS 
from sqlalchemy.orm import sessionmaker


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/error'
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Error(db.Model):
    __tablename__ = 'error'

    EID = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(64), nullable=False)

    # Lay Foo - commented out the constructor
    # def __init__(self, EID, message):
    #     self.EID = EID
    #     self.message = message

    def json(self):
        return {"EID": self.EID, "message": self.message}

#end of my code#

def receiveError():
    amqp_setup.check_setup()
    
    queue_name = "Error"  

    # set up a consumer and start to wait for coming messages
    amqp_setup.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    amqp_setup.channel.start_consuming() # an implicit loop waiting to receive messages; 
    #it doesn't exit by default. Use Ctrl+C in the command window to terminate it.

def callback(channel, method, properties, body): # required signature for the callback; no return
    print("\nReceived an error by " + __file__)
    processError(body)
    print() # print a new line feed

def processError(errorMsg):
    print("Printing the error message:")
    try:
        # Lay Foo - the following line converts errorMsg (json text) to a python dictionary
        error = json.loads(errorMsg)
        print("--JSON:", error)

        #start of my code#
        # Lay Foo - replace
        # Was: error_record = Error(1, error)
        # To: 
        error_record = Error(message=errorMsg)

        db.session.add(error_record)
        db.session.commit()
        #end of my code#
    except Exception as e:
        print("Exception:", e)
        print("--DATA:", errorMsg)
    print()


if __name__ == "__main__":  # execute this program only if it is run as a script (not by 'import')    
    print("\nThis is " + os.path.basename(__file__), end='')
    print(": monitoring routing key '{}' in exchange '{}' ...".format(monitorBindingKey, amqp_setup.exchangename))
    receiveError()
