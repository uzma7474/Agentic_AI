# basic example with conditional edge (branching)

from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    number: int
    result: str

def get_number(state: State):
    return state

def handle_even(state: State):
    return {"result": f"{state['number']} is even"}

def handle_odd(state: State):
    return {"result": f"{state['number']} is odd"}

def route(state: State):
    return "even" if state['number'] % 2 == 0 else "odd"

# create a graph
graph = StateGraph(State)

# add the nodes
graph.add_node("get_number", get_number)
graph.add_node("handle-even", handle_even)
graph.add_node("handle-odd", handle_odd)

# add the edges
graph.add_edge(START, "get_number")
graph.add_conditional_edges("get_number", route, {"even": "handle-even", "odd": "handle-odd"})
graph.add_edge("handle-even", END)
graph.add_edge("handle-odd", END)

# compile the graph
app = graph.compile()

# save the graph as image
image = app.get_graph().draw_mermaid_png()
with open("graphs/program2.png", "wb") as file:
    file.write(image)

# invoke the app
print(app.invoke({"number": 5}))
print(app.invoke({"number": 8}))