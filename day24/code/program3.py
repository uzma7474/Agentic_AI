from crewai import Agent, Task, Crew, LLM
from crewai.tools import tool, BaseTool

# create ollama LLM
llm = LLM(model="ollama/qwen2.5:7b", base_url="http://localhost:11434/v1")

# create a weather tool
@tool()
def get_weather(city: str):
    """Returns weather condition of a selected city"""
    data = {
        "pune": "rainy,20c",
        "mumbai": "overcast, 30c"
    }

    if city.lower() in data:
        return data[city.lower()]
    else:
        return "Weather condition is not available"

# create a stock price tool
@tool()
def get_stock_price(stock_symbol: str):
    """Returns the current stock price"""
    data = {
        "AAPL": "$450",
        "MSFT": "$400"
    }

    if stock_symbol in data:
        return data[stock_symbol]
    else:
        return "Stock price is not available"    


class MyTool(BaseTool):
    def _run(self, city: str):
        return "30c, rainy"


# define the agent
agent = Agent(
    role="Multi tool agent",
    goal="answer users query usig get_stock_price and get_weather tools",
    backstory="You are having an access to get_stock_price and get_weather tools",
    llm=llm,
    tools=[get_stock_price, get_weather]
)

# create a task
task = Task(description="""Answer following question:
    - what is the weather in Pune like?
    - what is the current price of AAPL?""",
    expected_output="from the list of tools, one will be executed. You captuer the result.",
    agent=agent
)

# create the crew
crew = Crew(
    agents=[agent],
    tasks=[task],
    verbose=True
)

# start the crew
response = crew.kickoff()
print(response)