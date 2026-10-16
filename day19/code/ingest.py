from config import EMBEDDING_MODEL, CHROMA_COLLECTION, CHROMA_DB, KNOWLEDGE_BASE

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from langchain_ollama import OllamaEmbeddings

import logging
from pathlib import Path
from langchain_chroma import Chroma

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

def load_documents():
    # load the documents into the list
    documents = []

    # check if the knowledge base exists
    knowledge_base_directory = Path(KNOWLEDGE_BASE)
    if not knowledge_base_directory.exists():
        logger.error(f"{knowledge_base_directory} is not present")
        return documents

    # load the files from the directory
    for file_path in knowledge_base_directory.iterdir():
        logger.info(f"reading file: {file_path}")
        loader = TextLoader(str(file_path))
    
        # load contents
        contents = loader.load()
        documents.append(contents[0])

    return documents


def split_documents(documents):
    # create the splitter
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    # split the documents
    return splitter.split_documents(documents)

def ingest_file(file_path):
    logger.info(f"started loading file {file_path}")
    loader = TextLoader(str(file_path))

    # load contents
    contents = loader.load()
    
    # create the splitter
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    # split the documents
    chunks = splitter.split_documents(contents)

    # add the newly adde chunks
    ids = []
    for index, chunk in enumerate(chunks):
        chunk.metadata.update({
            "chunk_index": index,
            "type": "IT"
        })
        ids.append(chunk)

    # vector_store.add_documents(documents=chunks, id=ids)
    vector_store.add_documents(documents=chunks)

    logger.info('-' * 80)
    logger.info(f"ingestion completed")

def ingest_all_files():
    # get all the documents
    documents = load_documents()

    # splitting the documents into chunk
    chunks = split_documents(documents)

    # add the documents to the vector store
    ids = []
    for index, chunk in enumerate(chunks):
        chunk.metadata.update({
            "chunk_index": index,
            "type": "IT"
        })
        ids.append(chunk)

    # vector_store.add_documents(documents=chunks, id=ids)
    vector_store.add_documents(documents=chunks)

    logger.info('-' * 80)
    logger.info(f"ingestion completed")

if __name__ == '__main__':
    ingest_all_files()