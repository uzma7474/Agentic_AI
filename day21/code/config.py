import os
from dotenv import load_dotenv

# load all env variables from .env file
load_dotenv()

MODEL = os.getenv('MODEL', 'qwen2.5:7b')