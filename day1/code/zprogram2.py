from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

provider = os.environ['PROVIDER']
print(f"provider = {provider}")

if provider == 'ollama':
    llm = ChatOllama(model="gemma:2b")
elif provider == 'openai':
    llm = ChatOpenAI(model="gpt-4")
    
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