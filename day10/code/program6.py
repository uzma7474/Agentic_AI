# use of short term memory

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
with open("graphs/program6.png", "wb") as file:
    file.write(image)

# create configuration
config = {"configurable": {"thread_id": "session1"}}

# invoke the app
# every invoke will create a new state object
result = app.invoke(
    {"messages": [HumanMessage(content="hi, my name is Amit.")]},
    config=config)

# print the last message only
print(result['messages'][-1].content)
print()

# since the first invocation is ended earlier, state also gets cleared
# the next statement will start a new state
result2 = app.invoke(
    {"messages": [HumanMessage(content="What is my name.")]},
    config=config)

# print the last message only
print(result2['messages'][-1].content)

