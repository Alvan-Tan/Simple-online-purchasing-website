import json
import os

import amqp_setup
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import requests
from invokes import invoke_http

import amqp_setup
import pika
import json

from datetime import datetime

monitorBindingKey='*.order'

shipping_URL = "http://localhost:5003/shipping/create_record"

order_json = {
            "AID": 11,
            "OID": 11,
            "product_name": "B sneaker",
            "quantity" : 1,
            "total_price": 20,
            "datetime": datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
            "payment_status" : "paid",
            "address": "234 Tanjong Pagar road",
            
            }
shipping_json = {
                "AID" : order_json["AID"],
                "OID" : order_json["OID"],
                "product_name" : order_json["product_name"],
                "payment_status" : order_json["payment_status"],
                "address" :order_json["address"],
                "datetime" :order_json["datetime"]
                }

# 4. Create shipping record
print('\n\n-----Invoking shipping microservice-----')      

shipping_status = invoke_http(shipping_URL, method="POST", json=shipping_json)  

# Check the payment status, if fail, cancel transaction.
code = shipping_status["code"]
message = json.dumps(order_json)
print(code)

if code in range (200, 300):
    print('\n\n-----Shipping record creation successful, invoke order microservice-----')
    
    #Send order details to order microservice
    amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="successful.order", 
        body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
    # make message persistent within the matching queues until it is received by some receiver 
    # (the matching queues have to exist and be durable and bound to the exchange)

   
