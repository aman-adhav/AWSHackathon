import math
import sagemaker as sage
import os
import requests
from sagemaker import get_execution_role
from sagemaker import transformer
from sagemaker import model
from src.model_package_arns import ModelPackageArnProvider
from sagemaker import ModelPackage
from io import BytesIO

import boto3
import json
import ast

def compare_price(actual_price, third_party_price, json_format):
    if actual_price > third_party_price:
        percent_diff = 1 - third_party_price/actual_price
        if percent_diff < 0.7:
            if json_format["is_used_product"] == "true":
                json_body = {"fake_product_message": "We compared your selling price to other retailers in the market and it seems to be significantly lower. Please update the description and the title. In your description you must include the appropriate reason to sell at a lower price."
                }
                return json_body
            elif json_format["is_used_product"] == "false":
                json_body = {"fake_product_message": "We compared your selling price to other retailers in the market and it seems to be significantly lower. Is this a used product? If so please mark this product as used/refurbished. Please update the description and the title. In your description you must include the appropriate reason to sell at a lower price."}
        else:
            return {"fake_product_message": "All Clear"}
    return {"fake_product_message": "All Clear"}


def truth_detector(text, text2):
    comprehend = boto3.client(service_name='comprehend',
                              region_name='us-east-1')
    product_val = json.dumps(
        comprehend.detect_key_phrases(Text=text, LanguageCode='en'),
        sort_keys=True, indent=8)
    product_values = ast.literal_eval(product_val)
    product_phrases = []
    for i in product_values['KeyPhrases']:
        product_phrases.append(i["Text"].lower())

    print(product_phrases)

    customer_val = json.dumps(
        comprehend.detect_key_phrases(Text=text2, LanguageCode='en'),
        sort_keys=True, indent=8)
    customer_values = ast.literal_eval(customer_val)
    customer_phrases = []
    for i in customer_values['KeyPhrases']:
        customer_phrases.append(i["Text"].lower())

    intersection = list(set(product_phrases) & set(customer_phrases))
    percent = len(intersection) / len(customer_phrases)

    if percent > 0.7:
        return 0
    else:
        return 1
