from langchain.chat_models import init_chat_model
from langgraph.graph import START, END, StateGraph, MessagesState
from langchain.messages import HumanMessage
from langgraph.checkpoint.sqlite import SqliteSaver

from dotenv import load_dotenv

# load all env variables from .env file
load_dotenv()

# create the model
model = init_chat_model(
    model="qwen2.5:7b",
    model_provider="ollama"
)

# create a graph
graph = StateGraph(MessagesState)

# add nodes
def call_node(state: MessagesState):
    # get the response from LLM
    response = model.invoke(state["messages"])

    # return the updated state
    return {"messages": response}

graph.add_node("call_node", call_node)

# add edges
graph.add_edge(START, "call_node")
graph.add_edge("call_node", END)

# create SQLite store
with SqliteSaver.from_conn_string("./data/checkpoints.db") as checkpointer:

    # compile the graph
    app = graph.compile(checkpointer=checkpointer)

    # create the configuration
    config = {
        "configurable": {"thread_id": "conversation-1"}
    }

    while True:
        user_input = input("[user]> ")
        if user_input.lower() in ['exit', 'quit']:
            break

        # send the user input to the graph
        response = app.invoke({
            "messages": [HumanMessage(content=user_input)]
        }, config)

        print(f"[agent]: {response['messages'][-1].content}")
        print("")