from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os, sys
import requests
from invokes import invoke_http
import amqp_setup
import pika
import json
from datetime import datetime

app = Flask(__name__)

CORS(app)

account_URL = "http://localhost:5002/verify"
stock_URL = "http://localhost:5001/stock/minus/"
payment_URL = ""
order_URL = "http://localhost:5004/order/create_record"
shipping_URL = "http://localhost:5003/shipping/create_record"

#error_URL = "http://localhost:5004/error"

@app.route("/place_order", methods=['POST'])
def place_order():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            order = request.get_json()
            print("\nReceived an order in JSON:", order)

            # do the actual work
            # 1. Send order info {cart items}
            result = processPlaceOrder(order)
            print('\n------------------------')
            print('\nresult: ', result)
            return jsonify(result), result["code"]

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "place_order.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400

@app.route("/payment_successful", methods=['POST'])
def place_order_2():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            order = request.get_json()
            print("\nReceived an order in JSON:", order)

            # do the actual work
            # 1. Send order info {cart items}
            result = processPlaceOrder2(order)
            print('\n------------------------')
            print('\nresult: ', result)
            return jsonify(result), result["code"]

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "place_order.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400

def processPlaceOrder(order):
    # 1. Check if the user is logged in
    # Invoke the account microservice
    print('\n-----Invoking account microservice-----')
    user_json = {"token":order["authentication_token"]}
    user_status = invoke_http(account_URL, method="POST", json=user_json)
    print('user_status_results:', user_status["message"])
  
    # Check the order result; if a failure, send it to the error microservice.
    code = user_status["code"]
    message = json.dumps(user_status)

    if code not in range(200, 300):
        # Redirect user to log in page
        print('\n\n-----User not logged in-----')
        
        #invoke_http(error_URL, method="POST", json=order_result)
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="account.error", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
        # make message persistent within the matching queues until it is received by some receiver 
        # (the matching queues have to exist and be durable and bound to the exchange)

        # 3. Return error
        return {
            "code": 500,
            "data": {"user_status_results": user_status["message"]},
            "message": "User not logged in yet"
        }

    # 2. Check if there is stock, if have, deduct the stocks
    print('\n\n-----Invoking stock microservice-----')
    selected_stock = order["product_name"]
    stock_json = {"quantity":order["quantity"]}
    stock_status = invoke_http(stock_URL+selected_stock, method="PUT", json=stock_json)  

    # Check the stock result; if a failure, send it to the error microservice.
    code = stock_status["code"]
    message = json.dumps(stock_status)

    if code not in range(200, 300):
        # Do not have required stock
        print('\n\n-----Out of stock, invoking error microservice-----')
        
        #invoke_http(error_URL, method="POST", json=order_result)
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="stock.error", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
        # make message persistent within the matching queues until it is received by some receiver 
        # (the matching queues have to exist and be durable and bound to the exchange)

        # 3. Return error
        return {
            "code": 500,
            "data": {"stock_status": stock_status},
        }     
    # return render_template("payment/payment.html")
    return {
        "code": 201,
        "data": {
            "message": "Stock deduction successful, proceeding with payment."
        }
    }

def processPlaceOrder2(order):
    print('\n\n-----Invoking order microservice-----')      
    order_json = {
                        "AID": order["AID"],
                        "datetime": datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
                        "payment_status": order["payment_status"],
                        "product_name" : order["product_name"],
                        "quantity" : order["quantity"],
                        "total_price" : order["total_price"],
                        "address": order["address"]
                    }
    order_status = invoke_http(order_URL, method="POST", json=order_json) 

    code = order_status["code"]
    message = json.dumps(order_status)
    order["OID"] = order_status["data"]["OID"]
    

    if code not in range(200, 300):
        # Do not have required stock
        print('\n\n-----Order record creation failed, cancel transaction, invoke error microservice-----')
        
        #Send error details to error microservice
        
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="shipping.error", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
        # make message persistent within the matching queues until it is received by some receiver 
        # (the matching queues have to exist and be durable and bound to the exchange)

        # 3. Return error
        return {
            "code": 500,
            "data": {"order_status": order_status["message"]},
        }

    # 4. Create shipping record
    print('\n\n-----Invoking shipping microservice-----')      
    shipping_json = {
                        "AID": order["AID"],
                        "OID": order["OID"],
                        "product_name" : order["product_name"],
                        "payment_status": order["payment_status"],
                        "address": order["address"],
                        "datetime": datetime.now().strftime("%Y/%m/%d %H:%M:%S")
                    }
    shipping_status = invoke_http(shipping_URL, method="POST", json=shipping_json)  

    # Check the payment status, if fail, cancel transaction.
    code = shipping_status["code"]
    message = json.dumps(shipping_status)

    if code not in range(200, 300):
        # Do not have required stock
        print('\n\n-----Shipping record creation failed, cancel transaction, invoke error microservice-----')
        
        #Send error details to error microservice
        
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="shipping.error", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
        # make message persistent within the matching queues until it is received by some receiver 
        # (the matching queues have to exist and be durable and bound to the exchange)

        # 3. Return error
        return {
            "code": 500,
            "data": {"shipping_status": shipping_status["message"]},
        }
    
    # Shipment record created successfully, add details into order database
    # print('\n\n-----Shipping record creation successful, invoke order microservice-----')
    # order["datetime"] = shipping_json["datetime"]
    
    # #Send order details to order microservice
    # amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="successful.order", 
    #     body=json.dumps(order), properties=pika.BasicProperties(delivery_mode = 2)) 
    # # make message persistent within the matching queues until it is received by some receiver 
    # # (the matching queues have to exist and be durable and bound to the exchange)

    #redirect user to order completion page
    return {
        "code": 201,
        "data": {
            "message": "Order successful!"
        }
    }

        


if __name__ == "__main__":
    app.run(port="5000", debug=True)