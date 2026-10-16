from agents import Agent, SQLiteSession, Runner, set_default_openai_client, set_tracing_disabled
from openai import AsyncOpenAI
import asyncio
import json

# create the client
client = AsyncOpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

# set the default client
set_default_openai_client(client)
set_tracing_disabled(True)

# create an agent
agent = Agent(name="assistant",model="qwen2.5:7b")

async def main():

    # create a sqlite session
    session = SQLiteSession(session_id="1", db_path="./data/open_ai.db")

    while True:
        user_input = input("[user]> ")
        if user_input.lower() in ['exit', 'quit']:
            break
        
        # send the user input to the agent
        response = await Runner.run(agent, user_input, session=session)

        print(f"[agent]> {response.final_output}")
        print()

if __name__ == '__main__':
    asyncio.run(main=main())