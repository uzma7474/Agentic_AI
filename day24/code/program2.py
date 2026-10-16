from crewai import Crew, Agent, Task, LLM

# create a model 
llm = LLM(model="ollama/qwen2.5:7b", base_url="http://localhost:11434/v1")

# create an agent
agent_researcher = Agent(
    # set the persona of the agent
    role="Senior Research Specialist",

    # what the agent has to achieve
    goal="Find the accurate information of any topic",

    # set the context
    backstory="""
    You are a senior research specialist having 15 years of experience in
    gathering information from different sources.
    """,

    # list of tools
    tools=[],

    verbose=True,

    # configure the llm
    llm=llm
)

# define the task
task = Task(
    # describe the task
    description="""
    Research on the topic 'AI used in healthcare'.
    Gather the information on following points:
    - current application 
    - key benefits
    - major challenges
    - future trends
    """,

    # what the task should deliver
    expected_output="A comprehensive summary of the research",

    # set the agent to execute the task
    agent=agent_researcher,
    verbose=True
)

# create a crew
crew = Crew(
    # list of agents
    agents=[agent_researcher],

    # list of tasks
    tasks=[task],

    verbose=True
)

# start the crew
response = crew.kickoff()

# print the result
print(response)


