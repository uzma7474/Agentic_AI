from crewai import Crew, Process

from app_agents.generator import generator_agent
from tasks.generator import generator_task

from config import VERBOSE


# create the crew
generator_crew = Crew(
    # add the agents to used by the task
    agents=[generator_agent],

    # add the tasks the crew need to perform
    tasks=[generator_task],

    # perform the operation sequentially
    process=Process.sequential,

    verbose=VERBOSE
)