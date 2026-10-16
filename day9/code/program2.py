from typing import TypedDict
from langgraph.graph import START, END, StateGraph

# define the state
class State(TypedDict):
    text: str
    word_count: int
    summary: str

# node to count number of words in the text
def count_words(state: State):
    return {"word_count": len(state['text'].split())}

# node to summarize the #characters and #words
def summarize(state: State):
    summary = f"#words: {state['word_count']}, #characters: {len(state['text'])}"
    return {"summary": summary}

# create the graph
graph = StateGraph(State)

# add the nodes
# node requires 
# - name of the node
# - function of the node
graph.add_node("count_words", count_words)
graph.add_node("summarize", summarize)

# add the edges
graph.add_edge(START, "count_words")
graph.add_edge("count_words", "summarize")
graph.add_edge("summarize", END)

# create an app
app = graph.compile()

# save the graph
image = app.get_graph().draw_mermaid_png()
with open("program2.png", "wb") as file:
    file.write(image)

# invoke the graph
print(app.invoke({"text": "LangGraph is a framework used to create stateful agent."}))