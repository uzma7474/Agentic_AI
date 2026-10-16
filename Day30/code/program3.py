from agents import Agent, RunState, Runner, set_default_openai_client, set_tracing_disabled
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
    # load the previous state
    with open("./data/checkpoint.json", "r") as file:
        data = json.loads(file.read())

        # construct the state
        previous_state: RunState = await RunState.from_json(agent, data["state"])

    while True:
        user_input = input("[user]> ")
        if user_input.lower() in ['exit', 'quit']:
            break

        # add input from user
        previous_state.add_input(user_input)
        
        # send the user input to the agent
        response = await Runner.run(
            agent,
            previous_state)

        # create a state (checkpoint)
        state = response.to_state()

        # persist it in a json file
        with open("./data/checkpoint.json", "w") as file:
            file.write(json.dumps({"state": state.to_json()}))

        print(f"[agent]> {response.final_output}")
        print()


if __name__ == '__main__':
    asyncio.run(main=main())