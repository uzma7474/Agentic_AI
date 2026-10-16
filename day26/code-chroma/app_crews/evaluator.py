from crewai import Crew, Process

from app_agents.evaluator import evaluator_agent
from tasks.evaluator import evaluation_task

from config import VERBOSE

# create the crew
evaluator_crew = Crew(
    # add the agents to the crew
    agents=[evaluator_agent],

    # add the tasks to the crew
    tasks=[evaluation_task],


    process=Process.sequential,
    verbose=VERBOSE
)