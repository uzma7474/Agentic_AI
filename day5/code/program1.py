from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.messages import HumanMessage

# create model connection
model = init_chat_model(model="qwen2.5:7b", model_provider="ollama")

# create an agent
agent = create_agent(
    model=model, 
    system_prompt="you are a helpful assistant")

while True:
    query = input("> ")
    if query in ['exit', 'quit']:
        break

    # send the query to the agent
    response = agent.invoke({
        "messages": [HumanMessage(content=query)]
    })

    # print response
    print(response['messages'][-1].content)
