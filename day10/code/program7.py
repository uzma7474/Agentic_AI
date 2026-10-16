# simple chat application

from typing import TypedDict, Annotated
from operator import add
from langgraph.graph import StateGraph, START, END
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import InMemorySaver
from langchain.messages import HumanMessage

# create the model
model = init_chat_model(model="qwen2.5:7b", model_provider="ollama")

class State(TypedDict):
    messages: Annotated[list, add]

def answer(state: State):
    # send the question to the model and get the response
    response = model.invoke(state['messages'])

    # return the answer by updating the state
    return {"messages": [response]}

# create the graph
graph = StateGraph(State)

# add the nodes
graph.add_node("answer", answer)

# add the edges
graph.add_edge(START, "answer")
graph.add_edge("answer", END)

# create checkpointer
checkpointer = InMemorySaver()

# compile the graph
app = graph.compile(checkpointer=checkpointer)

# save the graph as image
image = app.get_graph().draw_mermaid_png()
with open("graphs/program7.png", "wb") as file:
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