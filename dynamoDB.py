import boto3
import ast
# dynamodb = boto3.resource('dynamodb')
#
# # s3 = boto3.resource('s3')
# # my_bucket = s3.Bucket('thirdparty-image-bucket')
# # for object_summary in my_bucket.objects.filter(Prefix="52ce57a6-6272-4e4e-91e5-d4bc0640a8bd/"):
# #     print(object_summary)
#
# string = "https://thirdparty-image-bucket.s3.amazonaws.com/52ce57a6-6272-4e4e-91e5-d4bc0640a8bd/cut.png"
#
# print(string.split("https://thirdparty-image-bucket.s3.amazonaws.com/"))
import requests



# barcode = "adsfsadf"
# val = requests.get("https://api.barcodelookup.com/v2/products?barcode="+ barcode +"&formatted=y&key=0as2xduw3qreu9avhfv2pva2qz3rbm")
# dict_str = val.content.decode("UTF-8")
# #print(type(dict_str), "sadfasdf" + dict_str+ "adfasdffad")
# if dict_str != "\n":
#     values = ast.literal_eval(dict_str)
#
#     json_body = values["products"][0]
#     value = {}
#     if "barcode_number" in json_body:
#         value["barcode"] = int(json_body["barcode_number"])
#
#     if "product_name" in json_body:
#         value["product_name"] = json_body["product_name"]
#
#     if "description" in json_body:
#         value['product_description'] = json_body['description']
#
#     if len(json_body["stores"]) > 1:
#         expensive = json_body["stores"][-1]["store_price"]
#         cheap = json_body["stores"][0]["store_price"]
#         value["expensive_version"] = expensive
#         value["cheap_version"] = cheap
#     elif len(json_body["stores"]) == 1:
#         value["version_in_market"] = json_body["stores"][0]["store_price"]
#
#     print(value)
# else:
#     print("No")

