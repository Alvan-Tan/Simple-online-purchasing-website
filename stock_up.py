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

preorder_URL = "http://localhost:5005/preorder/restock"
stock_URL = "http://localhost:5001/stock/add/"
order_URL = "http://localhost:5004/order/create_record"
shipping_URL = "http://localhost:5003/shipping/create_record"

#error_URL = "http://localhost:5004/error"

@app.route("/replenish_stock", methods=['PUT'])
def replenish_stock():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            order = request.get_json()
            print("\nReceived an order in JSON:", order)

            # do the actual work
            # 1. Send order info {cart items}
            result = processPreorder(order)
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
                "message": "stock_up.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400

def processPreorder(order):
    # Invoke the preorder microservice
    print('\n-----Invoking preorder microservice-----')
    preorder_json = {"product_name":order["product_name"], "new_stock":order["new_stock"]}
    status = invoke_http(preorder_URL, method="GET", json=preorder_json)
    # print(status)

    # Check the order result; if a failure, send it to the error microservice.
    code = status["code"]
    message = json.dumps(status)

    # cleared_preorders = status.message.split(" ")
    # cleared_preorders = int(cleared_preorders[0])
    cleared_preorders_list = status["data"]["preorders"]
    

    if code not in range(200, 300):
        # Redirect user to log in page
        print('\n\n-----There is an error, invoking error microservice -----')
        
        #invoke_http(error_URL, method="POST", json=order_result)
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="preorder.error", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
        # make message persistent within the matching queues until it is received by some receiver 
        # (the matching queues have to exist and be durable and bound to the exchange)

        # 3. Return error
        return {
            "code": 500,
            "data": {"status_results": status["message"]},
            "message": "Preorder fulfillment failed"
        }

    # 2. Add any remaining stocks back to stock microservice
    print('\n\n-----Invoking stock microservice-----')
    selected_stock = order["product_name"]
    stock_json = {"quantity":status["data"]["new_stock"]}
    stock_status = invoke_http(stock_URL+selected_stock, method="PUT", json=stock_json)  

    # Check the stock result; if a failure, send it to the error microservice.
    code = stock_status["code"]
    message = json.dumps(stock_status)

    if code not in range(200, 300):
        # Do not have required stock
        print('\n\n-----Adding stock error, invoking error microservice-----')
        
        #invoke_http(error_URL, method="POST", json=order_result)
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="stock.error", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
        # make message persistent within the matching queues until it is received by some receiver 
        # (the matching queues have to exist and be durable and bound to the exchange)

        # 3. Return error
        # return {
        #     "code": 500,
        #     "data": {"stock_status": stock_status},
        # } 
        #     

    # for every cleared preorder, invoke order microservice and shipping microservice
    for o in cleared_preorders_list:
        print('\n\n-----Invoking order microservice-----')
        order_json = {
                        "AID": o["AID"],
                        "datetime": datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
                        "payment_status": o["payment_status"],
                        "product_name" : o["product_name"],
                        "quantity" : o["quantity"],
                        "total_price" : o["total_price"],
                        "address": o["address"]
                    }
        order_status = invoke_http(order_URL, method="POST", json=order_json)  
        # print("order status:",order_status)

        # Check the stock result; if a failure, send it to the error microservice.
        code = stock_status["code"]
        message = json.dumps(order_status)
        o["OID"] = order_status["data"]["OID"]

        if code not in range(200, 300):
            # Do not have required stock
            print('\n\n-----Order record creation failed, invoke error microservice-----')
            
            #invoke_http(error_URL, method="POST", json=order_result)
            amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="stock.error", 
                body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
            # make message persistent within the matching queues until it is received by some receiver 
            # (the matching queues have to exist and be durable and bound to the exchange)

            # return {
            #     "code": 500,
            #     "data": {"order_status": order_status},
            # }
            continue

        # 4. Create shipping record
        print('\n\n-----Invoking shipping microservice-----')      
        shipping_json = {
                            "AID": o["AID"],
                            "OID": o["OID"],
                            "product_name" : o["product_name"],
                            "payment_status": o["payment_status"],
                            "address": o["address"],
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
            # return {
            #     "code": 500,
            #     "data": {"shipping_status": shipping_status["message"]},
            # }
            continue
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
            "message": "All successful!"
        }
    }

   
        


if __name__ == "__main__":
    app.run(port="5006", debug=True)