from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.agents.middleware import PIIMiddleware
from langchain.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command

# create a model
model = init_chat_model(model="qwen2.5:7b", model_provider="ollama")

# create an agent
agent = create_agent(
    model=model,
    system_prompt="""
    You are a helpful agent answering the users query.
    """,
    checkpointer=InMemorySaver(),
    middleware=[
        PIIMiddleware(
            "email", 
            strategy="redact",
            apply_to_output=True, 
            apply_to_input=True,
            apply_to_tool_results=True
        ),
        PIIMiddleware(
            "credit_card", 
            strategy="redact",
            apply_to_output=True, 
            apply_to_input=True,
            apply_to_tool_results=True
        )
    ]
)

# create a hard coded session
config = {"configurable": {"thread_id": "session1"}}

while True:
    # get input from user
    query = input("> ")
    if query in ['exit', 'quit']:
        break

    # send the query to the agent
    response = agent.invoke(
        {"messages": [HumanMessage(content=query)]},
        config=config
    )

    # print the response
    print(response['messages'][-1].content)
