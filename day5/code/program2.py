# short term memory

from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver

# create model connection
model = init_chat_model(model="qwen2.5:7b", model_provider="ollama")

# create a short term memory for the agent
checkpointer = InMemorySaver()

# create an agent
agent = create_agent(
    # use the InMemorySave scheme for remembering the information in the memory
    checkpointer=checkpointer,
    model=model, 
    system_prompt="you are a helpful assistant")


# create a configuration
config = {"configurable": {"thread_id": "session1"}}

while True:
    query = input("> ")
    if query in ['exit', 'quit']:
        break

    # send the query to the agent
    response = agent.invoke(
        # send the query messages
        {"messages": [HumanMessage(content=query)]},

        # send the session information
        config=config)

    # print response
    print(response['messages'][-1].content)
