import logging
import os
from dotenv import load_dotenv

# set the logging basic configurations
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(message)s"
)

# load all the env variables from .env file
load_dotenv()

# load the configuration
TAVILY_API_KEY=os.getenv('TAVILY_API_KEY')
OPENAI_API_KEY=os.getenv('OPENAI_API_KEY')