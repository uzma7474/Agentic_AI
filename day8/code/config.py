import logging
from dotenv import load_dotenv
import os

# load all env variables from .env file
load_dotenv()

# get the mysql env variables from .env
MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
MYSQL_USER = os.getenv('MYSQL_USER', 'root')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_DB = os.getenv('MYSQL_DB', 'customer_support_db')
MYSQL_PORT = os.getenv('MYSQL_PORT', 3306)

# get the llm env variables from .env
MODEL = os.getenv('MODEL', 'qwen2.5:7b')
MODEL_PROVIDER = os.getenv('MODEL_PROVIDER', 'ollama')

# get the rate limiter env variables from .env
MESSAGE_COUNT = int(os.getenv('MESSAGE_COUNT', 50))
MESSAGE_DURATION = int(os.getenv('MESSAGE_DURATION', 100))

# configure the logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-7s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        # show all the logs to the screen
        logging.StreamHandler(),
        # save all the logs to the file
        logging.FileHandler("logs/app.log")
    ]
)