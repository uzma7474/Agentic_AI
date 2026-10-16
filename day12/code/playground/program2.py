from agents import Agent, Runner, set_default_openai_client, set_tracing_disabled
from openai import AsyncOpenAI

# create a ollama client
ollama_client = AsyncOpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

# set the default OpenAI client
set_default_openai_client(ollama_client)

# disable the tracing 
set_tracing_disabled(True)

# create an agent
agent = Agent(
    name="assistant",
    instructions="you are a helpful agent",
    model="qwen2.5:7b"
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