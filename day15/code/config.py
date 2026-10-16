import logging
from dotenv import load_dotenv
from agents import AsyncOpenAI, set_default_openai_client, set_tracing_disabled
import os


# load all env variables from .env file
load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# read the configuration
MODEL = os.getenv("MODEL", "qwen2.5:7b")
MODEL_PROVIDER = os.getenv("MODEL_PROVIDER", "ollama")
OLLAMA_BASE_URL = os.getenv('OLLAMA_BASE_URL')

MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_DB = os.getenv('MYSQL_DB')


# set the default openai client
ollama_client = AsyncOpenAI(
    base_url=OLLAMA_BASE_URL,
    api_key="ollama"
)

set_default_openai_client(ollama_client)
set_tracing_disabled(True)