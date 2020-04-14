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
from AWSHackathon.damage_detect import get_damage_prediction
from uuid import uuid4
app = Flask(__name__)
CORS(app)
s3 = boto3.resource('s3')
dynamodb = boto3.resource('dynamodb')
sage_client = boto3.client('sagemaker-runtime')
shipped = dynamodb.Table("shipped")


@app.route("/arrival_inspection_check", methods=["POST"])
def check_for_damage():
    val = ""
    dynamodb = []
    for filename, file in request.files.items():
        #print(file.filename)
        response = sage_client.invoke_endpoint(
            EndpointName='barcode-reader-rat',
            Body=file,
            ContentType='image/jpeg',
            Accept='application/json'
        )

        #print(response["Body"].read().decode("utf-8"))
        val = response["Body"].read().decode("utf-8")
        val = ast.literal_eval(val)

    if len(list(val.keys())) == 1:
        try:
            response = shipped.get_item(
                Key={'username': 'delivery_representative', 'product_id': list(val.keys())[0]},
            )
            dynamodb_items = response["Item"]
            print(dynamodb_items)
            values = {}
            values["username"] = "delivery_representative"
            values['shipment_id'] = dynamodb_items['shipment_id']
            values["delivery_not_damaged"] = False
            values["address"] = dynamodb_items["address"]
            values["product_id"] = list(val.keys())[0]
            return jsonify(values), 200
        except ClientError as e:
            print(e.response['Error']['Message'])
            return "Error Occured", 400

    return "Something went wrong", 200

@app.route("/upload_to_check_damage/<id_>", methods=["POST"])
def upload_to_check_damage(id_):
    for filename, file in request.files.items():
        #print(file.filename)
        s3.Bucket('thirdparty-image-bucket').put_object(Key=id_+"-delivery/"+file.filename, Body=file)
        s3Client = boto3.client("s3", region_name="us-east-1")
        object_acl = s3.ObjectAcl("thirdparty-image-bucket", id_+"-delivery/"+file.filename)
        response = object_acl.put(ACL='public-read')
        val = get_damage_prediction("https://thirdparty-image-bucket.s3.amazonaws.com/" + id_+"-delivery/"+file.filename)
        dict_str = val.decode("UTF-8")
        values = ast.literal_eval(dict_str)
        if values["prediction"] == "damaged":
            return jsonify({"state": 'There seems to be damage. Check for error to overide claim.'}), 200

    return jsonify({"state": 'No Damage Detected'}), 200

@app.route('/update/<id_>', methods=['POST'])
def update_product(id_):
    product_id = id_
    val = request.get_data()
    dict_str = val.decode("UTF-8")
    values = ast.literal_eval(dict_str)
    required = ["delivery_not_damaged", "stat"]
    if not all(k in values for k in required):
        return 'Missing values', 400

    try:
        retrieve = shipped.update_item(
            Key={'username': 'delivery_representative', 'product_id': product_id},
            UpdateExpression="set delivery_not_damaged=:p, stat=:a",
            ExpressionAttributeValues={
                ':p': values['delivery_not_damaged'],
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
    parser.add_argument('-p', '--port', default=5002, type=int,
                        help='port to listen on')
    args = parser.parse_args()
    port = args.port
    app.run(host='0.0.0.0', port=port)
