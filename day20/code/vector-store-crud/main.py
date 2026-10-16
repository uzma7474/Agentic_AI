from config import LLM_MODEL, EMBEDDING_MODEL, CHROMA_COLLECTION, CHROMA_DB, KNOWLEDGE_BASE, CHUNK_OVERLAP_SIZE, CHUNK_SIZE

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from langchain_ollama import OllamaEmbeddings

import logging
from pathlib import Path
from langchain_chroma import Chroma

from langchain.chat_models import init_chat_model
import json

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

# create the splitter
splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP_SIZE
)

def ingest_file(file_path: str, doc_type: str):
    logger.info(f"ingesting file: {file_path} with doc_type = {doc_type}")

    # create a loader
    loader = TextLoader(str(file_path))

    # load contents
    contents = loader.load()

    # split the document
    chunks = splitter.split_documents(contents)

    # add the newly added chunks
    for index, chunk in enumerate(chunks):
        chunk.metadata.update({
            "source": file_path,
            "chunk_index": index,
            "doc_type": doc_type
        })

    # add the documents to the vector store
    vector_store.add_documents(documents=chunks)
    logger.info('-' * 50)

def ingest_all_files():
    # create the path
    path = Path(KNOWLEDGE_BASE)

    # get all the files and directories
    for item in path.iterdir():
        if item.is_dir():
            for file_path in item.iterdir():
                ingest_file(str(file_path.resolve()), item.name)

    logger.info("Ingested all the documents")
    logger.info('')

def get_all_documents_ingested(required_doc_type: str = ''):
    # read the list of documents
    documents = vector_store.get()

    # read the metadata of all the documents
    sources = sorted({(item['doc_type'], item['source']) for item in documents['metadatas']})
    for doc_type, source in sources:
        if len(doc_type) == 0:
            print(f"{doc_type:<10} {source.split('/')[-1]}")
        elif doc_type == required_doc_type:
            print(f"{doc_type:<10} {source.split('/')[-1]}")
    print('-' * 80)

def ask(question: str):
    # get the type of document from llm
    response = model.invoke(f"""
    You are document experts. User is asking following question:

    {question}

    Based on the question tell me the which category the question belongs to.
    Your options are: HR, IT and Accounts.

    Answer the question in valid json format with key as "category".
    Do not return anything else.
    """)

    logger.info(f"category = {response.content}")

    result = json.loads(response.content)
    
    # find the result based on the query and doc type with score
    # score:
    # 0.0 to 0.5: best match
    # 0.5 to 1.0: somewhat related
    # 1.0 to 1.5: less related
    # >1.5: irrelevant 
    results = vector_store.similarity_search(
        query=question, 
        k=3, 

        # search within the documents of certain type
        filter={"doc_type": result['category']}
    )

    context = []
    for item in results:
        context.append(item.page_content)

    # ask the question to llm and get final answer
    response = model.invoke(f"""
    you are a helpful assistant. User has asked following question:
    \n
    {question}
    \n
    Following are the sources to answer the question:
    \n
    {context}
    \n
    Answer the question based on the sources provided.
    If the sources are not sufficient to answer the question, do not hallucinate or fabricate the result, instead say "I dont know".
    """)

    print(f"\n{response.content}")
    print()

def delete_chunks_by_source(source: str):
    logger.info(f"deleting chunks of document: {source}")
    vector_store.delete(where={"source": source})
    logger.info("deleted chunks from vectore store")

def update_existing_chunks(source: str, doc_type: str):
    # delete existing version
    delete_chunks_by_source(source)

    # add the file again
    ingest_file(source, doc_type)

if __name__ == '__main__':
    # while True:
    #     print("1. ingest all files")
    #     print("2. delete existing source")
    #     print("3. update existing source")
    #     print("4. ask question")

    # ingest_all_files()
    # get_all_documents_ingested('HR')
    ask("what are the new holiday plan")
    # delete_chunks_by_source('/Volumes/MyData/Sunbeam/2026/August/workshops/ai-o-04-agenticai/day20/code/vector-store-crud/knowledge-base/HR/performance-review.md')
    # print()

    # update_existing_chunks('/Volumes/MyData/Sunbeam/2026/August/workshops/ai-o-04-agenticai/day20/code/vector-store-crud/knowledge-base/HR/leave-policy.md', 'HR')
    # get_all_documents_ingested('HR')