from agents import Agent

# junior_agent
junior_agent = Agent(
    name="Junior Agent",
    instructions="You are a junior python developer having no experience. Generate the code for user's requirement.",
    model="gpt-4o"
)

# senior_agent
senior_agent = Agent(
    name="Senior Agent",
    instructions="""
    You are a senior python developer having 15 yrs of experience. 
    Generate the code for user's requirements with best performance.
    User best possible algorithms to get the best performance.""",
    model="gpt-5"
)

# final_agent: used to check the best answer
final_agent = Agent(
    name="Final Agent",
    instructions="""
    You are a python expert having 20 years experience.
    Choose the best code from the given list of codes.""",
    model="gpt-5.6"
)