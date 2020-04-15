import hashlib
import json
from time import time
from urllib.parse import urlparse
from uuid import uuid4
from flask_cors import CORS
import requests
from flask import Flask, jsonify, request
import boto3
import ast
import decimal
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
from sentiment_analyzer import truth_detector

app = Flask(__name__)
CORS(app)
s3 = boto3.resource('s3')
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
complaints = dynamodb.Table('complaints')
sage_client = boto3.client('sagemaker-runtime')
shipped = dynamodb.Table("shipped")
purchased = dynamodb.Table("purchased")


@app.route("/send_complaint/<id_>", methods=["POST"])
def send_complaint(id_):
    val = request.get_data()
    dict_str = val.decode("UTF-8")
    values = json.loads(dict_str)
    complaints.put_item(Item={
        'complaint_description': values["description"],
        'username': 'customer',
        'product_id': id_,
        'was_box_damaged': values["box_damaged"],
        'was_product_fake': values["product_fake"],
        'was_product_damaged': values["product_damaged"],
        'stat': "Complaint Sent"
    })

    return jsonify({"message": "If you are satisfied with your complaint please press the 'Review' Button"}), 200


def retrieve_regular(id_):
    folder_id = id_
    my_bucket = s3.Bucket('thirdparty-image-bucket')
    delivery_items = []
    vendor_items = []
    complaint_items = []
    try:
        response = shipped.get_item(
            Key={'username': 'delivery_representative', 'product_id': folder_id},
        )
        delivery_items = response
        # print(dynamodb_items)
    except ClientError as e:
        print(e.response['Error']['Message'])
        return "Error Occured", 400

    try:
        response = purchased.get_item(
            Key={'username': 'admin', 'product_id': folder_id},
        )
        vendor_items = response
        # print(dynamodb_items)
    except ClientError as e:
        print(e.response['Error']['Message'])
        return "Error Occured", 400

    try:
        response = complaints.get_item(
            Key={'username': 'customer', 'product_id': folder_id},
        )
        complaint_items = response
        # print(dynamodb_items)
    except ClientError as e:
        print(e.response['Error']['Message'])
        return "Error Occured", 400

    return delivery_items, vendor_items, complaint_items


@app.route('/review_complaint/<id_>', methods=["POST"])
def complaint_review(id_):
    delivery, vendor, complaint = retrieve_regular(id_)
    delivery = delivery["Item"]
    vendor = vendor["Item"]
    complaint = complaint["Item"]

    if complaint["was_box_damaged"] == "true" and delivery["delivery_not_damaged"] == "true":
        return jsonify({"message": "The box was not damaged upon delivery. If you believe the box was damaged, a customer service representative will contact you."}), 200
    elif complaint["was_box_damaged"] == "false":
        if complaint['was_product_damaged'] == "true":
            val = truth_detector(
                vendor["product_description"], complaint["complaint_description"])
            if val == 0:
                return jsonify({"message": "In the product description the vendor listed similar defects as you mentioned. If you would still like a refund a customer service representative will contact you."}), 200
            else:
                return jsonify({"message": "A customer service representative will contact you shortly."}), 200
    else:
        return jsonify({"message": "A customer service representative will contact you shortly."}), 200


if __name__ == '__main__':

    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5003, type=int,
                        help='port to listen on')
    args = parser.parse_args()
    port = args.port
    app.run(host='0.0.0.0', port=port)
