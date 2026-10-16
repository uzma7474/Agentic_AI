import os
import shutil

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

import config
import pdf_extractor


def get_vectorstore():
    embeddings = HuggingFaceEmbeddings(model_name=config.EMBEDDING_MODEL)
    return Chroma(
        collection_name=config.COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=config.CHROMA_FOLDER,
    )


def list_documents(vectorstore):
    """Return the sorted list of distinct source filenames currently stored
    in the knowledge base."""
    stored = vectorstore.get(include=["metadatas"])
    sources = {meta["source"] for meta in stored["metadatas"] if meta.get("source")}
    return sorted(sources)


def add_document(vectorstore, pdf_path):
    chunks = pdf_extractor.extract_all_chunks(pdf_path)
    if not chunks:
        return 0
    ids = [chunk.metadata["doc_id"] for chunk in chunks]
    vectorstore.add_documents(documents=chunks, ids=ids)
    return len(chunks)


def delete_document(vectorstore, filename):
    vectorstore.delete(where={"source": filename})
    stem = os.path.splitext(filename)[0]
    image_dir = os.path.join(config.IMAGES_FOLDER, stem)
    if os.path.isdir(image_dir):
        shutil.rmtree(image_dir)


def update_document(vectorstore, pdf_path):
    filename = os.path.basename(pdf_path)
    delete_document(vectorstore, filename)
    return add_document(vectorstore, pdf_path)
