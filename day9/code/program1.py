from typing import TypedDict
from langgraph.graph import START, END, StateGraph

# define the state which will be shared across the nodes
# TypeDict
# - is dictionary with key-value pairs
# - it enforces the nodes to see the predefined keys
class State(TypedDict):
    message: str

# node
# - every node will get an access to the state
# - execute the code and update the state if required
# - must return the (updated or same) state
def greet(state: State):
    print(f"inside greet function: {state}")
    return {"message": f"hello, {state['message']}"}


# build the graph
# while creating the graph, mention the state which every node will accept
graph = StateGraph(State)

# add the nodes
graph.add_node("greet", greet)

# add the edges
graph.add_edge(START, "greet")
graph.add_edge("greet", END)

# compile the graph and create an app
app = graph.compile()

# draw the graph
image = app.get_graph().draw_mermaid_png()
with open("program1.png", "wb") as file:
    file.write(image)

# send the message to the app to get the final result
# invoke at the end will return the updated state
print(app.invoke({"message": "amit"}))