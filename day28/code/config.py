from dotenv import load_dotenv
import os

# load the env variables from .env file
load_dotenv()

# load the config parameters
MODEL = os.getenv('MODEL')
MODEL_PROVIDER = os.getenv('MODEL_PROVIDER')
VERBOSE = True if os.getenv('VERBOSE').lower() == 'true' else False