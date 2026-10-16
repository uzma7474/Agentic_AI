from agents import Agent, Runner
from dotenv import load_dotenv

# load all the variables from .env file
load_dotenv()

# create an agent
agent = Agent(
    name="assistant",
    instructions="you are a helpful agent",
    model="gpt-4o"
)

while True:
    # get user input
    user_input = input("> ")
    if user_input in ['exit', 'quit']:
        break

    # send the input to the agent
    response = Runner.run_sync(
        starting_agent=agent,
        input=user_input
    )
    print(f"[agent]> {response.final_output}")
    print()