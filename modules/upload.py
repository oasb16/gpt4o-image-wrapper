import boto3
from modules.env import AWS_REGION, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, S3_BUCKET

s3 = boto3.client("s3", region_name=AWS_REGION,
                  aws_access_key_id=AWS_ACCESS_KEY_ID,
                  aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

def upload_file_to_s3(file_obj, filename):
    s3.upload_fileobj(file_obj, S3_BUCKET, filename)
    return f"https://{S3_BUCKET}.s3.{AWS_REGION}.amazonaws.com/{filename}"
