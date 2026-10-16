from agents import Agent, Runner, SQLiteSession
from dotenv import load_dotenv

# load all the environment variables from .env file
load_dotenv()

# select the model
MODEL = "gpt-4o"

# create session memory
session = SQLiteSession("session1")

# create multiple agents

# billing agent to handle all billing related queries
billing_agent = Agent(
    name="Billing Agent",
    instructions="you are a billing agent expert in handling all the billing related queries",
    model=MODEL
)

# refund agent to handle all refund related queries
refund_agent = Agent(
    name="Refund Agent",
    instructions="you are a refund agent expert in handling all refund related queries",
    model=MODEL
)

# triage agent to decide which agent to invoke
triage_agent = Agent(
    name="Triage Agent",
    instructions="""
    you are the first point of contact in the application.
    route the billing related questions to the Billing Agent and refund related questions to Refund Agent
    """,
    model=MODEL,
    handoffs=[billing_agent, refund_agent]
)

while True:
    # get user input
    user_input = input("> ")
    if user_input in ['exit', 'quit']:
        break

    # send the query to the triage agent
    response = Runner.run_sync(
        starting_agent=triage_agent,
        input=user_input,
        session=session
    )

    # find the agent used to answer the question
    print(f"[{response.last_agent.name}]> {response.final_output}")
    print()