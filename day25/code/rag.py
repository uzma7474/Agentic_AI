from langchain.chat_models import init_chat_model
from config import MODEL, MODEL_PROVIDER
from retriever import retriever

# connect to the ollama model
model = init_chat_model(model=MODEL, model_provider=MODEL_PROVIDER)

def answer_question(query: str):
    # get the context built by loading the documents from knowledge base
    documents = retriever(query)

    # build the context
    context = [f"source: {document.page_content}\n\n" for document in documents]

    # build the prompt
    prompt = f"""
    You are an IT support assistant.

    Answer the user's question using ONLY the provided context.
    If the answer cannot be found in the context, say:
    "I don't have enough information in the knowledge base."

    Do not invent information.

    Context:
    --------------------
    {context}
    --------------------

    User question:
    {query}

    Answer:
    """

    # invoke the question
    result = model.invoke(prompt)

    print(f"result = {result.content}")


if __name__ == '__main__':
    answer_question("what is kuberneted deployment?")