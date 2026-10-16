from agents import Agent
from tools import fetch_pull_request_diff
from config import REVIEWER_MODEL, CRITIC_MODEL
from prompts import REVIEWER_SYSTEM, CRITIC_SYSTEM
from dataclasses import dataclass
from typing import Literal

@dataclass
class EvaluationFeedback:
    """structured output from the critic agent"""
    feedback: str
    score: Literal['pass', 'needs_improvement']

# review agent
reviewer_agent = Agent(
    name="Review Agent",
    instructions=REVIEWER_SYSTEM,
    tools=[fetch_pull_request_diff],
    model=REVIEWER_MODEL
)

# critic agent
critic_agent = Agent(
    name="Critic Agent",
    instructions=CRITIC_SYSTEM,
    model=CRITIC_MODEL,
    output_type=EvaluationFeedback
)