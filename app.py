import hashlib
import json
from time import time
from urllib.parse import urlparse
from uuid import uuid4
from flask_cors import CORS
import requests
from flask import Flask, jsonify, request
import pymongo
import gridfs

app = Flask(__name__)
CORS(app)
client = pymongo.MongoClient("mongodb+srv://uofthacks:hack4th3sky@cluster0-hzrwe.mongodb.net/test?retryWrites=true&w=majority")
admin_list = client["AWSHackathon"]
fs = gridfs.GridFS(admin_list)
thi_parties = admin_list["online_shops"]
products = admin_list["id"]


@app.route("/")
def index():
    return '''
    	<form method="POST" action="/products/text" enctype="multipart/form-data">
    		<input type="text" name="profile_id">
    		<input type="file" name="barcode">
    		<input type="submit">
    	<form>
        '''


@app.route('/products/<id_>', methods=['POST'])
def product(id_):
    print(request)
    if "barcode" in request.files:
        barcode = request.files["barcode"]
        profile_id = request.form["profile_id"]
        fs.put(barcode)
        products.insert_one({"product_id": id_, "barcode_file": barcode.filename, "profile_id": profile_id})

    return "Done"


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int,
                        help='port to listen on')
    args = parser.parse_args()
    port = args.port
    app.run(host='0.0.0.0', port=port)







