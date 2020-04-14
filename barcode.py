import sagemaker as sage
import os
import boto3
from sagemaker import get_execution_role
from sagemaker import transformer
from sagemaker import model
from AWSHackathon.src.model_package_arns import ModelPackageArnProvider
from sagemaker import ModelPackage
import qrcode
import io


# client = boto3.client('sagemaker-runtime')
#
# file = open("data/test_files/QRcode_example5.jpg", "rb")
#
# response = client.invoke_endpoint(
#     EndpointName='barcode-reader-rat',
#     Body=file,
#     ContentType='image/jpeg',
#     Accept='application/json'
# )
#
# print(response["ContentType"])
# print(response["Body"].read().decode("utf-8"))

product_id = "920049234028930"
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
s3.Bucket('thirdparty-image-bucket').put_object(Key=product_id+"/qr_code_tags.jpg", Body=byteIO.getvalue())
