from dotenv import load_dotenv
import os

load_dotenv()

ACCESS_KEY = os.environ['AWS_ACCESS_KEY']
SECRET_KEY = os.environ['AWS_SECRET_KEY']
BUCKET_NAME = os.environ['AWS_BUCKET_NAME']
SESSION_TOKEN = os.environ['AWS_SESSION_TOKEN']