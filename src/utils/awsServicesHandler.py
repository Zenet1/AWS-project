import boto3
from utils.awsConfig import ACCESS_KEY, SECRET_KEY, REGION, SESSION_TOKEN

s3_handler = boto3.client('s3', aws_access_key_id = ACCESS_KEY, aws_secret_access_key = SECRET_KEY, aws_session_token = SESSION_TOKEN)

dynamodb_handler = boto3.resource(
    'dynamodb', 
    region_name = REGION, 
    aws_access_key_id = ACCESS_KEY, 
    aws_secret_access_key = SECRET_KEY, 
    aws_session_token = SESSION_TOKEN
    )

sns_handler = boto3.client(
    'sns', 
    region_name = REGION, 
    aws_access_key_id = ACCESS_KEY, 
    aws_secret_access_key = SECRET_KEY, 
    aws_session_token = SESSION_TOKEN
    )
