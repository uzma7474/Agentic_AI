from agents import (
    Agent, 
    Runner,
    function_tool,
    set_default_openai_client, 
    set_tracing_disabled, 
)
from openai import AsyncOpenAI
from langchain_chroma import Chroma
from config import LLM_MODEL, EMBEDDING_MODEL, CHROMA_COLLECTION, CHROMA_DB, KNOWLEDGE_BASE
from langchain_ollama import OllamaEmbeddings

# creating embedding model
embedding_model = OllamaEmbeddings(model=EMBEDDING_MODEL)

# create the client
client = AsyncOpenAI(
    base_url="http://localhost:11434/v1", 
    api_key="ollama"
)

# set the default client
set_default_openai_client(client=client)

# disable the tracing
set_tracing_disabled(True)

# load the vector store
vector_store = Chroma(
    persist_directory=CHROMA_DB,
    collection_name=CHROMA_COLLECTION,
    embedding_function=embedding_model
)

@function_tool
def load_knowledge(user_query: str):
    """
    Description:
        used to retrieve the knowledge (documents) from knowledge store
    Arguments:
        user's query to retrieve the documents from knowledge store
    Returns:
        knowlege requied to answer user's query
    """

    # find the similar documents to answer user's question
    docs = vector_store.similarity_search(
        query=user_query, k=5
    )

    # collect the contents
    result = []
    for doc in docs:
        result.append(doc.page_content)

    return result


def main():

    # create an agent
    agent = Agent(
        name="RAG agent",
        model=LLM_MODEL,
        instructions=f"""
            You are a helpful assistant. 

            You have an access to a tool named load_knowledge.
            Use that tool to answer the user's query.

            Do NOT use your own knowledge to answer user's query.
            If the knowledge is not sufficient then say: "I don't know".

            Never hallucinate the information.
        """,
        tools=[load_knowledge]
    )

    while True:
        # get user input
        user_query = input("> ")
        if user_query in ['exit', 'quit']:
            break

        # send the query to the agent
        respone = Runner.run_sync(
            starting_agent=agent,
            input=user_query
        )

        # print the response
        print(f"[agent]> {respone.final_output}")
        print("")

if __name__ == '__main__':
    main()