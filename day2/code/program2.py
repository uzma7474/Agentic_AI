from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
import os

# load all the configurations from .env file
load_dotenv()

# get the configuration
model = os.environ['MODEL']
model_provider = os.environ['MODEL_PROVIDER']

# create the llm connection
llm = init_chat_model(model=model, model_provider=model_provider)

# get input from user
query = input("> ")

# send the query to the model
response = llm.invoke(query)

# print the response
print(response.content)
