import os
import json
import boto3
import click
from botocore.exceptions import ClientError

DEFAULT_KEYS = [
    "OPENAI_API_KEY", "AWS_REGION", "AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY",
    "S3_BUCKET", "DYNAMODB_TABLE", "COGNITO_USER_POOL_ID", "COGNITO_APP_CLIENT_ID", "REDIRECT_URI"
]

@click.group()
def cli():
    pass

@cli.command()
@click.option("--project", prompt="Project name", help="Name of the project to generate secrets for")
def generate(project):
    secret_data = {key: f"<{key.lower()}_value>" for key in DEFAULT_KEYS}
    filename = f".env.{project}.json"
    with open(filename, "w") as f:
        json.dump(secret_data, f, indent=2)
    click.echo(f"✅ Generated secret template: {filename}")

@cli.command()
@click.option("--project", prompt="Project name", help="Name of the project to push secrets for")
def push(project):
    filename = f".env.{project}.json"
    if not os.path.exists(filename):
        click.echo(f"❌ Secret file {filename} not found.")
        return
    with open(filename) as f:
        secrets = json.load(f)

    secret_name = f"streamtoolkit/{project}"
    client = boto3.client("secretsmanager", region_name=secrets.get("AWS_REGION", "us-east-1"))

    try:
        client.create_secret(Name=secret_name, SecretString=json.dumps(secrets))
        click.echo(f"✅ Created secret: {secret_name}")
    except ClientError as e:
        if e.response["Error"]["Code"] == "ResourceExistsException":
            client.update_secret(SecretId=secret_name, SecretString=json.dumps(secrets))
            click.echo(f"♻️  Updated existing secret: {secret_name}")
        else:
            raise

@cli.command()
def list():
    client = boto3.client("secretsmanager", region_name="us-east-1")
    secrets = client.list_secrets(MaxResults=100)
    for secret in secrets.get("SecretList", []):
        if secret["Name"].startswith("streamtoolkit/"):
            click.echo("🔐 " + secret["Name"])

@cli.command()
@click.option("--project", prompt="Project name", help="Name of the project to pull secrets for")
def pull(project):
    secret_name = f"streamtoolkit/{project}"
    client = boto3.client("secretsmanager", region_name="us-east-1")
    try:
        response = client.get_secret_value(SecretId=secret_name)
        secrets = json.loads(response["SecretString"])
        with open(f".env.{project}.json", "w") as f:
            json.dump(secrets, f, indent=2)
        click.echo(f"⬇️  Pulled and saved secrets to .env.{project}.json")
    except ClientError as e:
        click.echo(f"❌ Could not retrieve secret: {secret_name}")
        raise e

@cli.command()
@click.option("--project", prompt="Project name", help="Name of the project to check secrets for")
def check(project):
    secret_name = f"streamtoolkit/{project}"
    client = boto3.client("secretsmanager", region_name="us-east-1")
    try:
        response = client.get_secret_value(SecretId=secret_name)
        secrets = json.loads(response["SecretString"])
        missing = [key for key in DEFAULT_KEYS if key not in secrets]
        if missing:
            click.echo(f"⚠️  Missing keys: {', '.join(missing)}")
        else:
            click.echo("✅ All required keys are present.")
    except ClientError:
        click.echo(f"❌ Secret not found: {secret_name}")
