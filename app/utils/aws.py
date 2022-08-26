import os

import boto3
from botocore.exceptions import NoCredentialsError


class S3Bucket:
    def __init__(self):
        self.access_key = os.environ.get('ACCESS_KEY')
        self.secret_key = os.environ.get('SECRET_KEY')

    def upload(self, file, bucket, s3_file) -> bool:
        s3 = boto3.client('s3', aws_access_key_id=self.access_key, aws_secret_access_key=self.secret_key)
        try:
            s3.upload_file(file, bucket, s3_file)
            return True
        except FileNotFoundError:
            return False
        except NoCredentialsError:
            return False
