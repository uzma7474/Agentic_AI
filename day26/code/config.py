from dotenv import load_dotenv
import os
import logging

# configure the logging instance
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(message)s"
)

# load the env variables from .env file
load_dotenv()

# load the configurations
PINCONE_INDEX = os.getenv('PINCONE_INDEX')
PINCONE_NAMESPACE = os.getenv('PINCONE_NAMESPACE')

KNOWLEDGE_SOURCE = os.getenv('KNOWLEDGE_SOURCE')
CHUNK_SIZE = int(os.getenv('CHUNK_SIZE'))
CHUNK_OVERLAP_SIZE = int(os.getenv('CHUNK_OVERLAP_SIZE'))
HF_MODEL_NAME = os.getenv('HF_MODEL_NAME')
MODEL = os.getenv('MODEL')
EVALUATOR_MODEL = os.getenv('EVALUATOR_MODEL')
GENERATOR_MODEL = os.getenv('GENERATOR_MODEL')
MODEL_PROVIDER = os.getenv('MODEL_PROVIDER')
VERBOSE = True if os.getenv('VERBOSE', 'true').lower() == 'true' else False
PINCONE_API_KEY = os.getenv('PINCONE_API_KEY')