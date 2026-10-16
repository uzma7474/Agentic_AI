# basic example with two nodes

from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    message: str

def first_node(state: State):
    return {"message": f"{state['message']}, first_node"}

def second_node(state: State):
    return {"message": f"{state['message']}, second_node"}

# create a graph
graph = StateGraph(State)

# add the nodes
graph.add_node("first_node", first_node)
graph.add_node("second_node", second_node)

# add the edges
graph.add_edge(START, "first_node")
graph.add_edge("first_node", "second_node")
graph.add_edge("second_node", END)

# compile the graph
app = graph.compile()

# save the graph as image
image = app.get_graph().draw_mermaid_png()
with open("graphs/program1.png", "wb") as file:
    file.write(image)

# invoke the app
print(app.invoke({"message": "initial message"}))
