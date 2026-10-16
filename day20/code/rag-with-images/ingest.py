from config import LLM_MODEL, EMBEDDING_MODEL, CHROMA_COLLECTION, CHROMA_DB, KNOWLEDGE_BASE
from langchain_ollama import OllamaEmbeddings

import logging
from pathlib import Path
from langchain_chroma import Chroma

from langchain.chat_models import init_chat_model
import json

from pdf_extractor import extract_all_chunks_from_pdf_file


# create the model
model = init_chat_model(model=LLM_MODEL, model_provider="ollama")

# logger instance
logger = logging.getLogger(__name__)

# creating embedding model
embedding_model = OllamaEmbeddings(model=EMBEDDING_MODEL)

# create the vector store
vector_store = Chroma(
    persist_directory=CHROMA_DB,
    collection_name=CHROMA_COLLECTION,
    embedding_function=embedding_model
)

def ingest_file(file_path: str):
    logger.info(f"started ingesting file: {file_path}")

    # get all textual and image chunks from the pdf file
    chunks = extract_all_chunks_from_pdf_file(file_path)

    # insert the documents into the vector store
    vector_store.add_documents(chunks)
    
    logger.info(f"finished ingesting file: {file_path}")

def ingest_documents():
    # create the path
    path = Path(KNOWLEDGE_BASE)

    # get all the files and directories
    for file_path in path.iterdir():
        ingest_file(file_path.resolve())

if __name__ == '__main__':
    ingest_documents()