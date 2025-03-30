import os
import json
import streamlit as st
import boto3
from botocore.exceptions import ClientError
from functools import lru_cache

SECRET_NAME = os.getenv("AWS_SECRET_VAULT", "streamtoolkit/default")
REGION_NAME = os.getenv("AWS_REGION", "us-east-1")

@lru_cache()
def fetch_secrets_from_aws():
    try:
        client = boto3.client("secretsmanager", region_name=REGION_NAME)
        response = client.get_secret_value(SecretId=SECRET_NAME)
        return json.loads(response["SecretString"])
    except ClientError as e:
        print("⚠️ AWS SecretsManager error:", e)
        return {}

def get_env(key: str, default=None):
    return (
        st.secrets.get(key)
        or os.getenv(key)
        or fetch_secrets_from_aws().get(key)
        or default
    )

OPENAI_API_KEY           = get_env("OPENAI_API_KEY")
AWS_REGION               = get_env("AWS_REGION")
AWS_ACCESS_KEY_ID        = get_env("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY    = get_env("AWS_SECRET_ACCESS_KEY")
S3_BUCKET                = get_env("S3_BUCKET")
DYNAMODB_TABLE           = get_env("DYNAMODB_TABLE")
COGNITO_USER_POOL_ID     = get_env("COGNITO_USER_POOL_ID")
COGNITO_APP_CLIENT_ID    = get_env("COGNITO_APP_CLIENT_ID")
REDIRECT_URI             = get_env("REDIRECT_URI")
