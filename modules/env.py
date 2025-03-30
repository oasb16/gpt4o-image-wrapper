import streamlit as st

OPENAI_API_KEY           = st.secrets["OPENAI_API_KEY"]
AWS_REGION               = st.secrets["AWS_REGION"]
AWS_ACCESS_KEY_ID        = st.secrets["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY    = st.secrets["AWS_SECRET_ACCESS_KEY"]
S3_BUCKET                = st.secrets["S3_BUCKET"]
COGNITO_USER_POOL_ID     = st.secrets["COGNITO_USER_POOL_ID"]
COGNITO_APP_CLIENT_ID    = st.secrets["COGNITO_APP_CLIENT_ID"]
DYNAMODB_TABLE           = st.secrets["DYNAMODB_TABLE"]
REDIRECT_URI             = st.secrets["REDIRECT_URI"]
