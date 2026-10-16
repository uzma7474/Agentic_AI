from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware, PIIMiddleware
from langchain.tools import tool
from langchain.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command

import os

@tool
def get_weather(city: str):
    """get weather for a city"""
    print("-> get_weather is called")
    data = {
        "pune": "22 cloudy",
        "mumbai": "18, overcast"
    }
    
    city = city.lower()

    if city in data:
        print(city)
        return data[city]
    
    print("Data not found")
    return "Data not found"

@tool
def send_email(sender: str, subject: str, body: str):
    """
    Description: sends an email to a sender
    Arguments
        sender: to whom the email will be sent
        subject: subject of email
        body: body of the email
    Returns: nothing
    """
    print("-> send_email is called")
    print(".. sending email ..")

@tool
def delete_file(path: str):
    """
    Description: delete a file on the path
    Arguments:
        path: file path needs to be deleted
    """
    print("-> delete_file is called")

    # delete a file
    # os.unlink(path)
    print(f"file deleted successfully ...")


# create a model
model = init_chat_model(model="qwen2.5:7b", model_provider="ollama")

# create an agent
agent = create_agent(
    model=model,
    tools=[get_weather, send_email, delete_file],
    system_prompt="""
    You are a helpful agent having access to get_weather, send_email and delete_file tools.
    Use the tools when required to answer the users query.
    """,
    checkpointer=InMemorySaver(),
    middleware=[
        # before calling the delete_file tool, 
        # agent will get the confirmation from user
        HumanInTheLoopMiddleware(
           interrupt_on={"delete_file": True, "send_email": True})
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

    # check if any interrupt is observed
    if '__interrupt__' in response:

        # get the interrupt object
        # Interrupt(value={'action_requests': [{'name': 'delete_file', 'args': {'path': '/tmp/info.txt'}, 'description': "Tool execution requires approval\n\nTool: delete_file\nArgs: {'path': '/tmp/info.txt'}"}], 'review_configs': [{'action_name': 'delete_file', 'allowed_decisions': ['approve', 'edit', 'reject', 'respond']}]}, id='8549f6d8d6eec370588f94a818db540f')
        interrupt = response['__interrupt__'][0]

        # get the tools information
        tool = interrupt.value['action_requests'][0]

        # print the approval message
        print(tool['description'])

        # get the decision input from user
        decision = input("Approve? (y/n): ")

        # check if user wants to approve
        if decision.strip().lower() == 'y':
            decision = {'type': 'approve'}
        else:
            decision = {'type': 'reject', 'message': 'user rejected the tool'}

        # send the confirmation to the agent
        result = agent.invoke(Command(resume={
                'decisions': [decision]
            }), config=config)

    # print the response
    print(response['messages'][-1].content)

