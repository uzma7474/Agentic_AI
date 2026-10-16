# long term memory
# pip install langgraph-checkpoint-sqlite

from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langgraph.checkpoint.sqlite import SqliteSaver

import sqlite3

# DB file name
DB_FILE="memory.db"

def create_sessions_table():
    # open the connection with the database
    connection = sqlite3.connect(DB_FILE)

    # get a cursor object
    cursor = connection.cursor()

    # create a table to store all the sessions
    cursor.execute("create table if not exists sessions (name text, thread_id TEXT);")

    # close the cursor
    cursor.close()

    # commit the changes
    connection.commit()

    # close the connection
    connection.close()

def create_new_session(session_name: str):
    # open the connection with the database
    connection = sqlite3.connect(DB_FILE)

    # get a cursor object
    cursor = connection.cursor()

    # create a table to store all the sessions
    cursor.execute("insert into sessions (name, thread_id) values (?, ?);", (session_name, session_name))

    # close the cursor
    cursor.close()

    # commit the changes
    connection.commit()

    # close the connection
    connection.close()

def load_all_sessions():
    # open the connection with the database
    connection = sqlite3.connect(DB_FILE)

    # get a cursor object
    cursor = connection.cursor()

    # create a table to store all the sessions
    cursor.execute("select thread_id, name from sessions;")

    # get all the rows
    rows = cursor.fetchall()
    temp_sessions = []
    for id, name in rows:
        temp_sessions.append({
            'thread_id': id, 
            'name': name
        })

    # close the cursor
    cursor.close()

    # close the connection
    connection.close()

    return temp_sessions

# create a table to store all sessions
create_sessions_table()

# maintain all the sessions
sessions = load_all_sessions()

# maintain the current session
current_session_id = None

# create model connection
model = init_chat_model(model="qwen2.5:7b", model_provider="ollama")

# create sqlite saver checkpointer
# SqliteSaver will store all the messages automatically
with SqliteSaver.from_conn_string(DB_FILE) as checkpointer:

    # create an agent
    agent = create_agent(
        # use the sqlite database for persisting the data across the application restart
        checkpointer=checkpointer,
        model=model, 
        system_prompt="you are a helpful assistant")

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

            # insert the session info in the sqlite database
            create_new_session(session_name)

            # add a new session to the sessions list
            sessions.append(session_name)

            # switch to the new session immediately
            current_session_id = session_name

        elif user_input == '/sessions':
            for index, session in enumerate(sessions):
                print(f"{index+ 1}. {session['thread_id']}")

        elif user_input.startswith('/switch'):
            # split the user_input to get the session name
            _, session_name = user_input.split(' ', maxsplit=1)

            # check if session_name is valid
            print([session['thread_id'] for session in sessions])
            if session_name in [session['thread_id'] for session in sessions]:
                # switch to selected session
                current_session_id = session_name
            else:
                print("invalid session name, please try again")

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
