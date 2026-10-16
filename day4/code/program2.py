from tools import get_current_time, get_daily_quote
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.messages import HumanMessage

# create a model
model = init_chat_model(
    model="qwen3.5:0.8b", 
    model_provider="ollama",
    temperature=0.3)

# create a list of tools
tools = [get_daily_quote, get_current_time]

# system prompt for agent
system_prompt = """
You are a helpful agent having an access to the tools. Use them when required.
Tools:
- get_daily_quote: use it for getting quote
- get_current_time: use it for getting time of user's machine

Rule
- use the required tool to get the job done
- if none of the tools give the correct answer, then just say "I dont know"
"""

# create an agent
agent = create_agent(
    model=model,
    tools=tools,
    system_prompt=system_prompt
)

while True:
    # get user input
    query = input("> ")
    if query in ['exit', 'quit']:
        break

    # send the query to the agent
    response = agent.invoke({
        "messages": [HumanMessage(content=query)]
    })

    # print the response
    print(f"response: {response['messages'][-1].content}")
    print('-' * 80)