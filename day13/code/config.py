from dotenv import load_dotenv
import os
import logging

# configure the logging instance
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s - %(message)s"
)

# get the logging instance
logger = logging.getLogger(__name__)

# load the environment variables from .env file
load_dotenv()

# get the configuration parameters
REVIEWER_MODEL = os.getenv("REVIEWER_MODEL", "qwen2.5:7b")
CRITIC_MODEL = os.getenv("CRITIC_MODEL", "qwen2.5:7b")
BASE_URL = os.getenv("BASE_URL", "http://localhost:11434/v1")
MAX_ITERATIONS = int(os.getenv("MAX_ITERATIONS", "2"))