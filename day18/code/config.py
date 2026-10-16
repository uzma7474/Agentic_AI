from dotenv import load_dotenv
import os

# load all env variables from .env file
load_dotenv()

# load mysql details
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DB = os.getenv("MYSQL_DATABASE")
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = int(os.getenv("MYSQL_PORT"))

# JWT related configurations
SECRET = os.getenv("SECRET")
ALGORITHM = os.getenv("ALGORITHM")
