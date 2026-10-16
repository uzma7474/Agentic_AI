# simulate the loop (calling a node multiple times)

from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    count: int
    target: int

def increment(state: State):
    print(f"state = {state}")
    return {"target": state["target"] + 1}

def route(state: State):
    return "done" if state['target'] >= state['count'] else "again"

# create the graph
graph = StateGraph(State)

# add the nodes
graph.add_node("increment", increment)

# add the edges
graph.add_edge(START, "increment")
graph.add_conditional_edges(
    "increment", route, {"again": "increment", "done": END})

# compile the graph
app = graph.compile()

# save the graph as image
image = app.get_graph().draw_mermaid_png()
with open("graphs/program3.png", "wb") as file:
    file.write(image)

# invoke the app
print(app.invoke({"count": 5, "target": 0}))