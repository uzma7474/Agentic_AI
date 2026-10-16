import asyncio
from agent_framework import Agent
from agent_framework.ollama import OllamaChatClient
from config import MODEL
import json

async def main():
    # create the client to connect to the LLM
    ollama_client = OllamaChatClient(model=MODEL)

    # create an agent
    agent = Agent(
        client=ollama_client,
        instructions="""
        You are a helpful agent. 
        Extract the information from the input given by user in the following JSON format:
        {"name": "string", "age": number, "address": "string", "email": "string"}

        Return only the JSON structure, nothing else.
        """,
        name="MyAgent"        
    )

    while True:
        # get input from user
        user_query = input("> ")
        if user_query in ['exit', 'quit']:
            break

        # send the query to the agent and get the response
        response = await agent.run(user_query)

        # remove the unwanted characters
        response = str(response).replace("```json", "").replace("```", "").strip()

        # convert the response into dictionary
        response = json.loads(response)

        print(f"name = {response['name']}")
        print(f"age = {response['age']}")
        print(f"address = {response['address']}")
        print(f"email = {response['email']}")

        print()

if __name__ == '__main__':
    asyncio.run(main())