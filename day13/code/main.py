from config import BASE_URL, MAX_ITERATIONS
import os
from openai import AsyncOpenAI
from agents import Runner, set_default_openai_client, set_tracing_disabled

from agent_definitions import reviewer_agent, critic_agent, EvaluationFeedback
import logging

from prompts import CRITIC_USER

from rich.console import Console
from rich.markdown import Markdown

# get the logging instance
logger = logging.getLogger(__name__)

# create the openai client
ollama_client = AsyncOpenAI(
    base_url=BASE_URL,
    api_key="ollama"
)

# set the default openai client
set_default_openai_client(ollama_client)

# disable tracing
set_tracing_disabled(True)

def validate_env_variables():
    if os.getenv("REVIEWER_MODEL") is None: raise Exception("REVIEWER_MODEL is missing in .env file")
    if os.getenv("CRITIC_MODEL") is None: raise Exception("CRITIC_MODEL is missing in .env file")
    if os.getenv("BASE_URL") is None: raise Exception("BASE_URL is missing in .env file")

# validate if all env variable are properly configured
validate_env_variables()

# create the rich console
console = Console()

while True:
    # get input from user
    user_input = input("enter PR url> ")
    if user_input in ['exit', 'quit']:
        break

    iteration = 1
    while iteration < MAX_ITERATIONS:
        # format input
        input_items = [
            {"role": "user", "content": f"Fetch and review the pull request at {user_input}"}
        ]

        # call the review agent
        logger.info(f"[Reviewer] generating the code review")
        review_result = Runner.run_sync(reviewer_agent, input_items)
        console.print(Markdown(review_result.final_output))
        console.print("-" * 80)

        # collect the review from the reviewer agent
        input_items = review_result.to_input_list()

        # add an instruction to the critic agent
        critic_input = CRITIC_USER.format(
            diff="(see the conversation to find the diff)",
            review=review_result.final_output
        )
        # add this instruction to the input_items
        input_items.append(
            {"role": "user", "content": critic_input}
        )

        # call the critic agent
        logger.info(f"[Critic] generating the code review") 
        critic_result = Runner.run_sync(
            critic_agent,
            input_items
        )

        # get the output from critic agent in the EvaluationFeedback type
        result: EvaluationFeedback = critic_result.final_output
        console.print(f"score = {result.score}")
            
        # check if critic agent considers this review is okay and wants to stop
        if result.score == 'pass':
            break

        # check if we are exhausted with the iterations
        if iteration == MAX_ITERATIONS:
            break

        iteration += 1

    console.print("-- final response --")
    console.print(Markdown(result.feedback))
    