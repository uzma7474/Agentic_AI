# install the langchain
# pip install langchain langchain-ollama langchain-openai


# import required packages
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

# load all the configurations from .env file
load_dotenv()

provider = os.environ['PROVIDER']
print(f"provider = {provider}")

if provider == 'ollama':
    # create an instance of ChatOllama
    llm = ChatOllama(
        # model name
        model="llama3.2:3b"
    )
elif provider == 'openai':
    llm = ChatOpenAI(model="gpt-4")

# infinite loop
while True:

    # user prompt
    prompt = input("> ")

    # check if user wants to exit
    if prompt in ['exit', 'quit', 'stop']:
        break

    # send the prompt to the model and generate the answer
    response = llm.invoke(prompt)

    # print the repsonse
    print(response.content)