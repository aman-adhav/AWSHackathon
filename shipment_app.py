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
import qrcode
import io
app = Flask(__name__)
CORS(app)
s3 = boto3.resource('s3')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('products')
purchased = dynamodb.Table("purchased")
sage_client = boto3.client('sagemaker-runtime')


def qr_code_generator(product_id):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(product_id)
    qr.make(fit=True)
    byteIO = io.BytesIO()
    img = qr.make_image(fill_color="black", back_color="white")
    print(img)
    s3 = boto3.resource('s3')
    img.save(byteIO, format='JPEG')
    s3.Bucket('thirdparty-image-bucket').put_object(
        Key=product_id + "-shipment/qr_code_tags.jpg", Body=byteIO.getvalue())
    return product_id + "-shipment/qr_code_tags.jpg"

@app.route("/ship_item/<id_>", methods=["GET"])
def ship_item(id_):
    product_id = id_
    shipment_qr = qr_code_generator(product_id)
    val = request.get_data()
    dict_str = val.decode("UTF-8")
    values = ast.literal_eval(dict_str)
    dynamodb_items = None
    try:
        retrieve = table.update_item(
            Key={'username': 'admin', 'product_id': product_id},
            UpdateExpression="set stat=:stat",
            ExpressionAttributeValues={
                ":stat": "Purchased",
            },
            ReturnValues="UPDATED_NEW"
        )

    except ClientError as e:
        print(e.response['Error']['Message'])

    try:
        response = table.get_item(
            Key={'username': 'admin', 'product_id': product_id},
        )
        dynamodb_items = response
    except ClientError as e:
        print(e.response['Error']['Message'])
        return "Error Occured", 400

    dynamodb_items = dynamodb_items["Item"]
    values['product_description'] = dynamodb_items["product_description"]
    values['username'] = 'admin'
    values['product_id'] = product_id
    values['product_name'] = dynamodb_items["product_name"]
    values['product_price'] = dynamodb_items["product_price"]
    values['is_used_product'] = dynamodb_items["is_used_product"]
    values['barcode'] = dynamodb_items["barcode"]
    values["agree_not_fake"] = False
    values["agree_not_damaged"] = False
    values["qr_code"] = "https://thirdparty-image-bucket.s3.amazonaws.com/"+ product_id + "-shipment/qr_code_tags.jpg"
    values["stat"] = "Not Shipped"
    #print(values)
    purchased.put_item(Item=values)

    return "Done", 200

@app.route('/retrieve_for_shipment/<id_>', methods=["POST"])
def retrieve(id_):
    folder_id = id_
    my_bucket = s3.Bucket('thirdparty-image-bucket')
    image_list = []
    dynamodb_items = []
    for object_summary in my_bucket.objects.filter(Prefix= id_+"-shipment/"):
        val = "https://thirdparty-image-bucket.s3.amazonaws.com/"+ object_summary.key
        image_list.append(val)
    try:
        response = purchased.get_item(
            Key={'username': 'admin', 'product_id': folder_id},
        )
        dynamodb_items = response
        #print(dynamodb_items)
    except ClientError as e:
        print(e.response['Error']['Message'])
        return "Error Occured", 400
    return jsonify({'image_list': image_list, "item_info": dynamodb_items}), 200


@app.route('/upload_for_shipment/<id_>', methods=['POST'])
def upload(id_):
    for filename, file in request.files.items():
        #print(file.filename)
        s3.Bucket('thirdparty-image-bucket').put_object(Key=id_+"-shipment/"+file.filename, Body=file)
    return '<h1>File saved to S3 </h1>'

@app.route('/check_for_damage/<id_>', method=['POST'])
def check_damage(id_):


@app.route('/update/<id_>', methods=['POST'])
def update_product(id_):
    product_id = id_
    val = request.get_data()
    dict_str = val.decode("UTF-8")
    values = ast.literal_eval(dict_str)
    required = ["agree_not_fake", "agree_not_damaged", "stat"]
    if not all(k in values for k in required):
        return 'Missing values', 400

    try:
        retrieve = purchased.update_item(
            Key={'username': 'admin', 'product_id': product_id},
            UpdateExpression="set agree_not_fake=:r, agree_not_damaged=:p, stat=:a",
            ExpressionAttributeValues={
                ':r': values['agree_not_fake'],
                ':p': values['agree_not_damaged'],
                ':a': values["stat"]
            },
            ReturnValues="UPDATED_NEW"
        )
        return "Done", 200
    except ClientError as e:
        print(e.response['Error']['Message'])

if __name__ == '__main__':

    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5001, type=int,
                        help='port to listen on')
    args = parser.parse_args()
    port = args.port
    app.run(host='0.0.0.0', port=port)
