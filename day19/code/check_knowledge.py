from langchain_chroma import Chroma
from config import EMBEDDING_MODEL, CHROMA_COLLECTION, CHROMA_DB, KNOWLEDGE_BASE
from langchain_ollama import OllamaEmbeddings

# creating embedding model
embedding_model = OllamaEmbeddings(model=EMBEDDING_MODEL)

    
# load the vector store
vector_store = Chroma(
    persist_directory=CHROMA_DB,
    collection_name=CHROMA_COLLECTION,
    embedding_function=embedding_model
)

# find the similar documents
docs = vector_store.similarity_search(
    "I am getting access denied error", k=2)
print(docs)