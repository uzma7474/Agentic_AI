from langchain_ollama import ChatOllama

# create the llm connection
llm = ChatOllama(model="llama3.2:3b")

# get input from user
query = input("> ")

# send the query to the model
response = llm.invoke(query)

# print the response
print(response.content)
