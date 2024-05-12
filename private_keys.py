import os

from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')

S_USER_EMAIL = os.environ.get('S_USER_EMAIL')
S_USER_PASSWORD = os.environ.get('S_USER_PASSWORD')
S_USER_FIRST_NAME = os.environ.get('S_USER_FIRST_NAME')
S_USER_LAST_NAME = os.environ.get('S_USER_LAST_NAME')

BROKER_URL = os.environ.get('BROKER_URL')
RESULT_BACKEND = os.environ.get('RESULT_BACKEND')

HOST_USER = os.getenv('EMAIL_HOST_USER')
HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
HOST = os.getenv('EMAIL_HOST')
PORT = os.getenv('EMAIL_PORT')
