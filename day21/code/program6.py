import asyncio
from agent_framework import Agent
from agent_framework.ollama import OllamaChatClient
from config import MODEL
from datetime import datetime

def get_current_time():
    """get the current time of the machine"""
    print("get_current_time is called")
    return f"{datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')}"

def get_weather(city: str):
    """get the current weather in the city"""
    data = {
        "pune": "rainy, 15c",
        "mumbai": "cloudy, 30c",
        "nashik": "overcast, 20c"
    }

    if city.lower() in data: 
        return data.get(city.lower())
    
    return "No weather information is available for this city"

def get_visa_requirement(country: str):
    """get the visa requirements for a country"""
    data = {
        "usa": "a visa is mandatory and can be created for 60 days a year",
        "china": "a visa is mandatory and can be created at least for 7 days",
        "maldives": "visa on arrival"
    }

    if country.lower() in data: 
        return data.get(country.lower())
    
    return "No visa information is available for this country"

async def main():
    # create the client to connect to the LLM
    ollama_client = OllamaChatClient(model=MODEL)

    # create an agent
    agent = Agent(
        client=ollama_client,
        instructions="You are a helpful agent. Answer users query.",
        name="MyAgent",
        tools=[get_visa_requirement, get_current_time, get_weather]
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