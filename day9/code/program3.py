from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    number: int
    result: str

# node to send the data (number)
def get_number(state: State):
    # pass the same state as it
    return state

# node to update the state the number is even
def node_even(state: State):
    # update the state with even result
    return {"result": f"{state['number']} is even"}

# node to update the state the number is odd
def node_odd(state: State):
    # update the state with odd result
    return {"result": f"{state['number']} is odd"}

# router to decide whether to go to even node or odd node
# this function is called as a router
def route(state: State):
    # return the status based on the calculation
    return "even" if state['number'] % 2 == 0 else "odd"

# create a graph
graph = StateGraph(State)

# add the node
graph.add_node("get_number", get_number)
graph.add_node("function_even", node_even)
graph.add_node("function_odd", node_odd)

# add the edges
graph.add_edge(START, "get_number")

# if route function returns "even" call node_even function
# if route function returns "odd" call node_odd function
graph.add_conditional_edges(
    "get_number", route, {"even": "function_even", "odd": "function_odd"})

graph.add_edge("function_odd", END)
graph.add_edge("function_even", END)

# compile the graph
app = graph.compile()

# draw the graph
image = app.get_graph().draw_mermaid_png()
with open("program3.png", "wb") as file:
    file.write(image)

# invoke the graph
print(app.invoke({"number": 10}))
print(app.invoke({"number": 11}))
