from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.messages import HumanMessage

# roles
# - system: used to set the tone/background/persona
# - user: used to send the query
# - ai: used to grab the result from LLM
# - tool: used to send the result from a tool to the LLM

# create llm connection
model = init_chat_model(
    model="llama3.2:3b", 
    model_provider="ollama",
    temperature=0.3)

# define the system prompt for the agent
system_prompt = """
You are a helpful agent answering user's query.
"""

# create an agent
agent = create_agent(
    model=model,
    system_prompt=system_prompt
)

# agent = create_agent(
#     model="ollama/llama3.2:3b",
#     system_prompt=system_prompt
# )

while True:
    # get input from user
    query = input("> ")
    if query in ['exit', 'quit']:
        break

    # send the query to model
    # response = agent.invoke({"messages": [
    #     {'role': 'user', 'content': query}
    # ]})
    response = agent.invoke({
        "messages": [HumanMessage(content=query)]
    })

    # read the last message which is the answer of the question
    final_response = response['messages'][-1]
    print(final_response.content)