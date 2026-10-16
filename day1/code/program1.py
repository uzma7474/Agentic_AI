# install the langchain
# pip install langchain langchain-ollama langchain-openai

# import required packages
from langchain_ollama import ChatOllama

# create an instance of ChatOllama
llm = ChatOllama(
    # model name
    model="gemma4:26b"
)

# user prompt
prompt = "what is the the weather of pune ?"

# send the prompt to the model and generate the answer
response = llm.invoke(prompt)

# print the repsonse
print(response.content)