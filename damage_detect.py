import sagemaker as sage
import os
import requests
import boto3
from sagemaker import get_execution_role
from sagemaker import transformer
from sagemaker import model
from src.model_package_arns import ModelPackageArnProvider
from sagemaker import ModelPackage
from io import BytesIO

from PIL import Image
import json
import numpy as np


def get_damage_prediction(image_url):
    response = requests.get(image_url)
    client = boto3.client('sagemaker-runtime', region_name='us-east-1')
    img = Image.open(BytesIO(response.content)).convert(mode='RGB')
    img = img.resize((300, 300))

    img = np.array(img).tolist()
    img_json = json.dumps({'instances': [{'input_image': img}]})

    prediction = client.invoke_endpoint(
        EndpointName='product-damage-detect-rat',
        Body=img_json,
        ContentType='application/json',
    )

    val = prediction["Body"].read()
    return val

    predictor = sage.RealTimePredictor(endpoint='product-damage-detect-rat',
                                       content_type='application/json')
    prediction = predictor.predict(img_json)

    return prediction
