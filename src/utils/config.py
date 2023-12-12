from dotenv import load_dotenv
import os

load_dotenv()

usuario = os.environ['DB_USER']
password = os.environ['DB_PASSWORD']
servidor = os.environ['DB_HOST']
puerto = os.environ['DB_PORT']
db = os.environ['DB_NAME']

database_connection_uri = f'mysql://{usuario}:{password}@{servidor}/{db}'