from agents import Agent, Runner, set_default_openai_client, set_tracing_disabled, function_tool, SQLiteSession
from openai import AsyncOpenAI

# create a ollama client
ollama_client = AsyncOpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

# set the default OpenAI client
set_default_openai_client(ollama_client)

# disable the tracing 
set_tracing_disabled(True)

# create a long term session memory
session_memory = SQLiteSession("session1", "conversation.db")

# a tool to get the current weather condition
@function_tool
def get_weather(city: str):
    """
    Description: get the current weather condition in the selected city.
    Arguments:
        city: name of the city to find the weather condition.
    Returns: current weather condition of the selectd city
    """
    return f"the current weather in {city} is rainy and temperature is 29°c"

@function_tool
def get_stock_price(symbol: str):
    """
    Description: get the stock price of a selected symbol.
    Arguments:
        symbol: the one whose stock price needs to be checked.
    Returns: current stock price of the selected symbol.
    """
    return f"the current stock price of {symbol} is $450"
 
# create an agent
agent = Agent(
    name="assistant",
    instructions="you are a helpful agent",
    model="qwen2.5:7b",
    tools=[get_weather, get_stock_price]
)

while True:
    # get user input
    user_input = input("> ")
    if user_input in ['exit', 'quit']:
        break

    # send the input to the agent
    response = Runner.run_sync(
        starting_agent=agent,
        input=user_input,
        session=session_memory
    )
    print(f"[agent]> {response.final_output}")
    print()