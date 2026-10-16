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
CHROMA_DB = os.getenv('CHROMA_DB')
KNOWLEDGE_SOURCE = os.getenv('KNOWLEDGE_SOURCE')
CHUNK_SIZE = int(os.getenv('CHUNK_SIZE'))
CHUNK_OVERLAP_SIZE = int(os.getenv('CHUNK_OVERLAP_SIZE'))
HF_MODEL_NAME = os.getenv('HF_MODEL_NAME')
CHROMA_COLLECTION_NAME = os.getenv('CHROMA_COLLECTION_NAME')
MODEL = os.getenv('MODEL')
MODEL_PROVIDER = os.getenv('MODEL_PROVIDER')