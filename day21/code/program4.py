import asyncio
from agent_framework import Agent
from agent_framework.ollama import OllamaChatClient
from config import MODEL

async def main():
    # create the client to connect to the LLM
    ollama_client = OllamaChatClient(model=MODEL)

    # create an agent
    agent = Agent(
        client=ollama_client,
        instructions="You are a helpful agent. Answer users query.",
        name="MyAgent"        
    )

    # create the session (short term memory)
    session = agent.create_session()

    while True:
        # get input from user
        user_query = input("> ")
        if user_query in ['exit', 'quit']:
            break

        # send the query to the agent and get the response
        # since the session is passed to the run method, 
        # it will remember the context
        response = await agent.run(user_query, session=session)
        print(f"[Agent]> {response}")
        print()

if __name__ == '__main__':
    asyncio.run(main())