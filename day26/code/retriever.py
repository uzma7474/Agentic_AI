from langchain_pinecone import PineconeVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from config import HF_MODEL_NAME, PINCONE_API_KEY, PINCONE_INDEX, PINCONE_NAMESPACE

def retrieve(query: str, k:int = 2):
    # create embedder
    embedding_function = HuggingFaceEmbeddings(
        model_name=HF_MODEL_NAME
    )

    # load the vector store
    vector_store = PineconeVectorStore(
        index_name=PINCONE_INDEX,
        embedding=embedding_function,
        namespace=PINCONE_NAMESPACE,
        pinecone_api_key=PINCONE_API_KEY
    )

    # search within the store
    results = vector_store.similarity_search(query, k=k)

    return results

def main():
    documents = retrieve("what is kuberneted deployment?")
    print(documents)

if __name__ == '__main__':
    main()