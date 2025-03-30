import boto3
from streamtoolkit_omkar.config.env import AWS_REGION, S3_BUCKET

s3 = boto3.client("s3", region_name=AWS_REGION)

def upload_file_to_s3(file_obj, filename):
    s3.upload_fileobj(file_obj, S3_BUCKET, filename)
    return f"https://{S3_BUCKET}.s3.{AWS_REGION}.amazonaws.com/{filename}"
