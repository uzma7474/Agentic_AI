from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from config import HF_MODEL_NAME, CHROMA_COLLECTION_NAME, CHROMA_DB

def retriever(query: str):
    # create embedder
    embedding_function =HuggingFaceEmbeddings(
        model_name=HF_MODEL_NAME
    )

    # load the vector store
    vector_store = Chroma(
        persist_directory=CHROMA_DB,
        collection_name=CHROMA_COLLECTION_NAME,
        embedding_function=embedding_function
    )

    # search within the store
    results = vector_store.similarity_search(query, k=2)

    return results

def main():
    documents = retriever("what is kuberneted deployment?")
    print(documents)

if __name__ == '__main__':
    main()