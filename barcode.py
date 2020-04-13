import sagemaker as sage
import os
import boto3
from sagemaker import get_execution_role
from sagemaker import transformer
from sagemaker import model
from AWSHackathon.src.model_package_arns import ModelPackageArnProvider
from sagemaker import ModelPackage


client = boto3.client('sagemaker-runtime')

file = open("data/test_files/QRcode_example5.jpg", "rb")

response = client.invoke_endpoint(
    EndpointName='barcode-reader-rat',
    Body=file,
    ContentType='image/jpeg',
    Accept='application/json'
)

print(response["ContentType"])
print(response["Body"].read().decode("utf-8"))

