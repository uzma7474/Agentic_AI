from agent_framework import Agent
from agent_framework.openai import OpenAIChatClient
from agent_framework.orchestrations import MagenticBuilder

from app_agents.budget import create_budget_agent
from app_agents.activities import find_activities_agent
from app_agents.flights import find_flights_agent
from app_agents.hotels import find_hotels_agent

from config import OPENAI_API_KEY

# create client
def create_client():
    return OpenAIChatClient(
        model="gpt-5",
        api_key=OPENAI_API_KEY
    )

def build_workflow() -> MagenticBuilder:
    # create the client
    client = create_client()

    # create the agents
    budget_agent = create_budget_agent(client=client)
    activity_agent = find_activities_agent(client=client)
    flight_agent = find_flights_agent(client=client)
    hotel_agent = find_hotels_agent(client=client)

    # create a supervisor agent
    supervisor = Agent(
        name="Supervisor",
        client=client,
        instructions=(
            "You are the travel planning supervisor.\n"
            "You coordinate specialists:\n"
            "  - flight_agent: flight search\n"
            "  - hotel_agent: hotel search\n"
            "  - activity_agent: activities matching interests\n"
            "  - budget_agent: budget tracking and currency conversion\n\n"
            "Workflow for every request (follow this exact order):\n"
            "  STEP 1: Call flight_agent for flight options.\n"
            "  STEP 2: Call hotel_agent for accommodations.\n"
            "  STEP 3: Call activity_agent for things to do.\n"
            "  STEP 4: Call budget_agent to total costs and compare to budget.\n"
            "  STEP 5: Synthesize the final itinerary.\n\n"
            "  CRITICAL RULES:\n"
            "  - Once an agent returns a result, that step is COMPLETE. Do not call it again.\n"
            "  - After calling flight_agent, move immediately to hotel_agent.\n"
            "  - After calling hotel_agent, move immediately to activity_agent.\n"
            "  - After calling activity_agent, move immediately to budget_agent.\n"
            "  - After calling budget_agent, synthesize the final answer immediately.\n"
            "  - You have exactly 4 agent calls. Do not exceed them.\n"
            "  - If an agent reports that sources do not provide the information, that is a\n"
            "    valid result. Record it as-is and move on; never re-run that agent.\n"
            "Final answer format (use these exact headings):\n"
            "## Trip Summary\n"
            "## Destinations\n"
            "## Flights\n"
            "## Hotels\n"
            "## Activities\n"
            "## Budget Breakdown\n"
            "## Notes\n\n"
            "Keep the final answer under 500 words."
        ),
    )

    # create the workflow
    workflow = MagenticBuilder(
        participants=[budget_agent, activity_agent, flight_agent, hotel_agent],
        manager_agent=supervisor,
        max_round_count=10,
        max_stall_count=3,
        max_reset_count=1
    ).build()

    return workflow