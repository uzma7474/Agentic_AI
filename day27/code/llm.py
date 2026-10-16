from config import MODEL, MODEL_PROVIDER
from langchain.chat_models import init_chat_model

# create the agent
model = init_chat_model(model=MODEL, model_provider=MODEL_PROVIDER)

def call_real_llm(messages):
    response = model.invoke(messages)
    return response.content