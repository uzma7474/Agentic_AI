# basic example with two nodes

from typing import TypedDict, Annotated
from operator import add
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    # messages here is a list
    # because of Annotated and add operator, the new message will get
    # added to the list instead of replacing the existing value
    messages: Annotated[list, add]

def first_node(state: State):
    # condition to clear the messages
    if len(state['messages']) > 20:
        state['messages'].clear()

    return {"messages": ["first_node"]}

def second_node(state: State):
    return {"messages": ["last_node"]}

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
with open("graphs/program4.png", "wb") as file:
    file.write(image)

# invoke the app
print(app.invoke({"messages": ["initial message"]}))
