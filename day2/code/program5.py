from langchain.tools import tool
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
import os

# load the configuration from .env file
load_dotenv()

# read the configs
model = os.environ['MODEL']
model_provider = os.environ['MODEL_PROVIDER']

@tool
def get_weather(city: str) -> str:
    """
    Description: this function is used to get weather information for a city.

    Arguments:
        param1 (city): city name for which the weather information is required.

    Returns: Weather information of a selected if available.
    """

    # temperature data
    data = {
        'pune': 'rainy with 22c temperature',
        'mumbai': 'rainy with 18c temperature',
        'delhi': 'cloudy with 6c temperature'
    }

    # get the city weather
    if city.lower() in data:
        return data[city.lower()]

    # city does not exist
    return f'weather information in {city} does not exist'


@tool
def get_stock_info(label: str) -> str:
    """
    Description: this tool is used to get the current stock information of a label.

    Arguments:
        param1 (label): label for which the stock information is required.

    Returns: the current stock information about the label.
    """

    # stock data
    data = {
        'AAPL': '$4T',
        'MSFT': '$3T'
    }

    # get the stock info
    if label.upper() in data:
        return data[label.upper()]

    return f"no stock information is available for {label}"


# create llm connection
llm = init_chat_model(model_provider=model_provider, model=model)

# bind the tool(s) with the llm
llm_with_tools = llm.bind_tools([get_weather, get_stock_info])

# get input from user
query = "what is current stock position of AAPL?"
print(f"query = {query}")

# send the prompt and get the response
response = llm_with_tools.invoke(query)

# check if the response has an attribute named tool_calls
if hasattr(response, 'tool_calls') and len(response.tool_calls) > 0:
    print("a tool is required to answer the query")
    # model is asking to execute a tool
    print(response.tool_calls)
else:    
    # print the response 
    print(f"no tool is required to answer the query")
    print(response.content)