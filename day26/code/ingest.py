from pathlib import Path
from config import KNOWLEDGE_SOURCE, HF_MODEL_NAME, CHUNK_OVERLAP_SIZE, CHUNK_SIZE, PINCONE_INDEX, PINCONE_NAMESPACE, PINCONE_API_KEY

from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

# load the path
path = Path(KNOWLEDGE_SOURCE)

# create the pinecone client
pinecone_client = Pinecone(api_key=PINCONE_API_KEY)

# set the HF embedding dimensions
DIMENSIONS = 384

def load_documents():
    documents = []

    # load the markdown documents from knowledge source
    for file in path.glob("*.md"):

        # read the contents of the file
        content = file.read_text()

        # append the newly read contents
        documents.append({
            "content": content,
            "source": file.name
        })

    return documents


def main():
    # load the documents
    documents = load_documents()

    # create the splitter
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP_SIZE
    )

    # create embedder
    embedding_function =HuggingFaceEmbeddings(
        model_name=HF_MODEL_NAME
    )

    # collect all the chunks
    chunks = []

    # create the chunks from all the documents
    for document in documents:
        # split the contents
        split_chunks = splitter.create_documents(
            [document['content']],
            metadatas=[{"source": document['source']}]
        )

        # append the chunks
        chunks.extend(split_chunks)

    # create the index first using required dimensions
    if not pinecone_client.has_index(PINCONE_INDEX):
        pinecone_client.create_index(
            name=PINCONE_INDEX,
            dimension=DIMENSIONS,
            metric="cosine",
            spec=ServerlessSpec(cloud='aws', region="us-east-1")
        )

    # get the vector store
    vector_store = PineconeVectorStore(
        index_name=PINCONE_INDEX,
        embedding=embedding_function,
        namespace=PINCONE_NAMESPACE,
        pinecone_api_key=PINCONE_API_KEY
    )

    vector_store.add_documents(chunks)
   
    # print the summary
    print(f"loaded #documents = {len(documents)}")
    print(f"created #chunks   = {len(chunks)}")
    print("successfully created vector db")

if __name__ == '__main__':
    main()