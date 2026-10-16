# use llm

from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain.chat_models import init_chat_model

# create the model
model = init_chat_model(model="qwen2.5:7b", model_provider="ollama")

class State(TypedDict):
    question: str
    answer: str

def answer(state: State):
    # send the question to the model and get the response
    response = model.invoke(state['question'])

    # return the answer by updating the state
    return {"answer": response.content}

# create the graph
graph = StateGraph(State)

# add the nodes
graph.add_node("answer", answer)

# add the edges
graph.add_edge(START, "answer")
graph.add_edge("answer", END)

# compile the graph
app = graph.compile()

# save the graph as image
image = app.get_graph().draw_mermaid_png()
with open("graphs/program5.png", "wb") as file:
    file.write(image)

# invoke the app
print(app.invoke({"question": "what is the color of sky?"}))