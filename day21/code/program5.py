import asyncio
from agent_framework import Agent
from agent_framework.ollama import OllamaChatClient
from config import MODEL
from datetime import datetime

def get_current_time():
    """get the current time of the machine"""
    print("get_current_time is called")
    return f"{datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')}"

async def main():
    # create the client to connect to the LLM
    ollama_client = OllamaChatClient(model=MODEL)

    # create an agent
    agent = Agent(
        client=ollama_client,
        instructions="You are a helpful agent. You have an access to a tool to get current time.",
        name="MyAgent",
        tools=get_current_time
    )

    while True:
        # get input from user
        user_query = input("> ")
        if user_query in ['exit', 'quit']:
            break

        # send the query to the agent and get the response
        response = await agent.run(user_query)
        print(f"[Agent]> {response}")
        print()

if __name__ == '__main__':
    asyncio.run(main())