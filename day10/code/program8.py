# simple chat application with tools support

from typing import TypedDict, Annotated
from operator import add
from langgraph.graph import StateGraph, START, END
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import InMemorySaver
from langchain.messages import HumanMessage, ToolMessage
from langchain.tools import tool

@tool
def get_weather(city: str):
    """
    Description: used to get weather information of a selected city
    Arguments:
        city: name of the city to get the weather information
    Returns: weather information of selected city
    """

    data = {
        "pune": "22c, cloudy",
        "mumbai": "18c, clear"
    }

    if city.lower() in data:
        return data[city.lower()]

    return f"no weather information available for {city}"


@tool
def get_stock(symbol: str):
    """returns the current stock price of the required symbol"""
    return f"the current stock price of {symbol} is $400"

# create a tool dictionary
tools = {
    "get_weather": get_weather,
    "get_stock": get_stock
}

# create the model
model = init_chat_model(model="qwen2.5:7b", model_provider="ollama")

# bind the tool(s) with llm
model = model.bind_tools([get_weather, get_stock])

class State(TypedDict):
    messages: Annotated[list, add]

def answer(state: State):
    # send the question to the model and get the response
    response = model.invoke(state['messages'])

    # return the answer by updating the state
    return {"messages": [response]}

def execute_tools(state: State):
    # get the last message
    message = state['messages'][-1]

    # collect all the tool_call results
    tool_messages = []

    # get the tool from tool_calls
    for tool in message.tool_calls:
        # get the tool name
        tool_name = tool['name']

        # get the tool args
        tool_args = tool['args']

        # get the tool function
        tool_function = tools[tool_name]

        # execute the tool
        result = tool_function.invoke(tool_args)

        # collect the answer
        tool_messages.append(ToolMessage(content=result, tool_call_id=tool['id']))

    return {"messages": tool_messages}
        

def route(state: State):
    # get the last message
    message = state['messages'][-1]

    # check if the tool_calls is present
    # check if tool call is required
    if hasattr(message, 'tool_calls') and message.tool_calls:
        return "tools"

    # tool call is not required, so end the invocation
    return "done"

# create the graph
graph = StateGraph(State)

# add the nodes
graph.add_node("answer", answer)
graph.add_node("execute_tools", execute_tools)

# add the edges
graph.add_edge(START, "answer")
graph.add_conditional_edges(
    "answer", route, {"tools": "execute_tools", "done": END})
graph.add_edge("execute_tools", "answer")

# create checkpointer
checkpointer = InMemorySaver()

# compile the graph
app = graph.compile(checkpointer=checkpointer)

# save the graph as image
image = app.get_graph().draw_mermaid_png()
with open("graphs/program8.png", "wb") as file:
    file.write(image)

# create configuration
config = {"configurable": {"thread_id": "session1"}}

while True:
    user_input = input("user > ")
    if user_input in ['quit', 'exit']:
        break

    # invoke the app
    # every invoke will create a new state object
    result = app.invoke(
        {"messages": [HumanMessage(content=user_input)]},
        config=config)

    # print the last message only
    print(f"agent > {result['messages'][-1].content}")
    print()