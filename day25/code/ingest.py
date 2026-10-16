from pathlib import Path
from config import KNOWLEDGE_SOURCE, HF_MODEL_NAME, CHROMA_COLLECTION_NAME, CHROMA_DB, CHUNK_OVERLAP_SIZE, CHUNK_SIZE

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

# load the path
path = Path(KNOWLEDGE_SOURCE)

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

    # add all the chunks to the vector store
    Chroma.from_documents(
        documents=chunks,
        embedding=embedding_function,
        persist_directory=CHROMA_DB,
        collection_name=CHROMA_COLLECTION_NAME
    ) 

    # print the summary
    print(f"loaded #documents = {len(documents)}")
    print(f"created #chunks   = {len(chunks)}")
    print("successfully created vector db")

if __name__ == '__main__':
    main()