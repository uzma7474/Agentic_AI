from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.tools import tool
from langchain.agents.middleware import AgentMiddleware
from langchain.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver
import logging

# create a logger
logger = logging.getLogger(__name__)


@tool
def get_weather(city: str):
    """get weather for a city"""
    print("-> get_weather is called")
    city = city.lower()
    data = {
        "pune": "22 cloudy",
        "mumbai": "18, overcast"
    }

    return data[city]

# create a custom middleware
class LoggingMiddleware(AgentMiddleware):
    """Middleware to log model calls and count them."""

    def before_agent(self, state, runtime):
        print(f"-- before agent --")
        return super().before_agent(state, runtime)

    def after_agent(self, state, runtime):
        print(f"-- after agent --")
        return super().after_agent(state, runtime)

    def before_model(self, state, runtime):
        print(f"-- before model --")
        return {"model_call_count": 1}

    def after_model(self, state, runtime):
        print("-- after model --")
        return None

# create a model
model = init_chat_model(model="qwen2.5:7b", model_provider="ollama")

# create an agent
agent = create_agent(
    model=model,
    system_prompt="""
    You are a helpful agent answering the users query.
    """,
    tools=[get_weather],
    checkpointer=InMemorySaver(),
    middleware=[LoggingMiddleware()]
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
