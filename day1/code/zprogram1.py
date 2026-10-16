from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="gemma:2b"
)

prompt = "what are the the coordinates of Nandurbar ?"

response = llm.invoke(prompt)

print(response.content)