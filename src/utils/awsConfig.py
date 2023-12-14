from dotenv import load_dotenv
import os

load_dotenv()

ACCESS_KEY = os.environ['AWS_ACCESS_KEY']
SECRET_KEY = os.environ['AWS_SECRET_KEY']
SESSION_TOKEN = os.environ['AWS_SESSION_TOKEN']
REGION = os.environ['AWS_REGION']
BUCKET_NAME = os.environ['AWS_BUCKET_NAME']
DYNAMODB_NAME = os.environ['AWS_DYNAMODB_NAME']
ARN_TOPIC = os.environ['AWS_ARN_TOPIC']