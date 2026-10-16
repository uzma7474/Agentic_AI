# short term memory

from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver

# create model connection
model = init_chat_model(model="qwen2.5:7b", model_provider="ollama")

# create a short term memory for the agent
checkpointer = InMemorySaver()

# create an agent
agent = create_agent(
    # use the InMemorySave scheme for remembering the information in the memory
    checkpointer=checkpointer,
    model=model, 
    system_prompt="you are a helpful assistant")

# maintain all the sessions
sessions = []

# maintain the current session
current_session_id = None

# print the menu
print("welcome to my chat application")
print("you can use the following commands")
print("/sessions              : get the list of sessions")
print("/new <session name>    : create a new session")
print("/switch <session name> : switch to the different session")
print("/exit or /quit         : quit the application")
print('-' * 80)

while True:
    user_input = input(f"[{current_session_id}]> ").strip()

    # check the commands
    if user_input in ['/exit', '/quit']:
        break

    elif user_input.startswith('/new'):
        # split the user_input to get the session name
        _, session_name = user_input.split(' ', maxsplit=1)

        # add a new session to the sessions list
        sessions.append(session_name)

        # switch to the new session immediately
        current_session_id = session_name

    elif user_input == '/sessions':
        for index, session in enumerate(sessions):
            print(f"{index+ 1}. {session}")

    elif user_input.startswith('/switch'):
        # split the user_input to get the session name
        _, session_name = user_input.split(' ', maxsplit=1)

        # switch to selected session
        current_session_id = session_name

    else: 

        # check if any session is active
        if current_session_id is None:
            # there is no session active
            print("please create a session first")
            continue

        # create a configuration
        config = {"configurable": {"thread_id": current_session_id}}

        # send the query to the agent
        response = agent.invoke(
            # send the query messages
            {"messages": [HumanMessage(content=user_input)]},

            # send the session information
            config=config)

        # print response
        print(response['messages'][-1].content)
        print()
