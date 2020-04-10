import sagemaker as sage
import os
import boto3
from sagemaker import get_execution_role
from sagemaker import transformer
from sagemaker import model
from src.model_package_arns import ModelPackageArnProvider
from sagemaker import ModelPackage
role = get_execution_role()

sess = sage.Session()

account = sess.boto_session.client('sts').get_caller_identity()['Account']
region = sess.boto_session.region_name

modelpackage_arn = ModelPackageArnProvider.get_model_package_arn(sess.boto_region_name)

# Define predictor wrapper class
def predict_wrapper(endpoint, session):
    return sage.RealTimePredictor(endpoint, session, content_type='image/jpeg')

# Create a deployable model
model = ModelPackage(role=role,
                                      model_package_arn = modelpackage_arn,
                                      sagemaker_session = sess,
                                      predictor_cls = predict_wrapper)
# ARN
print(modelpackage_arn)
file_name = 'data/test_files/my_barcode.jpg'
with open(file_name, "rb") as image:
  b = bytearray(image.read())

# Perform a prediction
result = predictor.predict(b).decode('utf-8')

# View the prediction
print(result)

bucket = sess.default_bucket()

transform_input_prefix = "barcode/validation"
TRANSFORM_WORKDIR = "data/transform"
# upload data from local directory to bucket

transform_input = sess.upload_data(TRANSFORM_WORKDIR, key_prefix=transform_input_prefix)

print ("Transform Data Location " + transform_input)

transformer = model.transformer(1, 'ml.m4.xlarge',
                                output_path="s3://"+bucket+"/barcode/batch-transform-output")
transformer.transform(transform_input, content_type='image/jpeg')
transformer.wait()

print("Batch Transform output saved to " + transformer.output_path)
