class ModelPackageArnProvider:

    @staticmethod
    def get_model_package_arn(current_region):
        mapping = {
          "us-east-1" : "arn:aws:sagemaker:us-east-1:063375884371:endpoint/barcode-reader-rat"
        }
        return mapping[current_region]
