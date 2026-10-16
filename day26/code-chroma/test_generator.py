from app_crews.generator import generator_crew
from retriever import retrieve
import logging

# create logger instance
logger = logging.getLogger(__name__)

def generate_answer(query: str):

    logger.info("Retrieving the documents")

    # retrieve the documents to build the context
    documents = retrieve(query=query, k=4)

    # build the context
    context = "\n\n".join([f"source: {document.page_content}" for document in documents])

    logger.info("generating the result")

    # kick off the crew
    response = generator_crew.kickoff(inputs={
        "question": query,
        "context": context
    })

    logger.info(response.raw)

    # return a structured result
    return {
        "query": query,
        "context": context,
        "answer": response.raw
    }

if __name__ == '__main__':
    result = generate_answer("what is kubernetes deployment?")
    print(f"result = {result}")