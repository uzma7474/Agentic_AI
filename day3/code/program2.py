import streamlit as st

from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

from dotenv import load_dotenv
import os

# load configuration from .env file
load_dotenv()

from tools import get_stock_info, get_weather, tell_me_a_joke, convert_currency

# get the configurations
model = os.environ['MODEL']
model_provider = os.environ['MODEL_PROVIDER']

# create a list of tools
tools = [get_stock_info, get_weather, tell_me_a_joke, convert_currency]

# create a dictionary to hold the tools metadata
tools_info = {tool.name: tool for tool in tools}

# create llm connection
llm = init_chat_model(model=model, model_provider=model_provider)

# bind the tools with the llm
llm = llm.bind_tools(tools)

# create a list of messages
messages = []

st.header("My Chatbot")
st.subheader("Ask any question")

# get input from user
query = st.chat_input("Enter your question")
if query:
    # print the query
    st.markdown(query)

    # append the query to the messages list
    messages.append(HumanMessage(content=query))

    # send the messages to the llm
    response = llm.invoke(messages)

    # check if llm wants to execute any tool
    if hasattr(response, 'tool_calls') and len(response.tool_calls) > 0:

        # execute every tool llm is asking to execute
        for tool in response.tool_calls:
            print(f"-> executing tool: {tool['name']}")

            # get the tool function
            tool_function = tools_info[tool['name']]

            # execute the tool function and get the result
            result = tool_function.invoke(tool['args'])
            # print(f"-> tool result: {result}")

            # append the tool result to the messages
            messages.append(ToolMessage(content=result, tool_call_id=tool['id']))
            # messages.append({
            #     'role': 'tool', 'tool_call_id': tool['id'], 'content': result
            # })
            # print(f"-> {messages}")
            
        # send the messages to the LLM again
        response = llm.invoke(messages)

        # print the result on UI
        st.markdown(response.content)

    else:
        print(f"-> no tool call is required")
        print(f"response: {response.content}")