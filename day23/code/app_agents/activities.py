from agent_framework import Agent
from app_agents.tavily_search_tool import tavily_search

def search_activities(
    city: str,
    interests: list[str],
    days: int = 3):
    """searches the activities within the city matching user's interests"""

    # get all interests
    all_interests = ', '.join(interests)

    # build the query
    query = f"""
    top {all_interests} activities and experiences within {city} 
    for {days} day trip
    """

    return tavily_search(query, max_results=6)


def find_activities_agent(client):
    """Creates an agent used to search hotels"""
    return Agent(
        name="Activities-Agent",
        client=client,
        instructions=(
            "You recommend activities matching user interests. Use search_activities. "
            "Return 4-6 activities with name, category, duration, and cost. "
            "You do NOT book activities; you only recommend them."
        ),
        tools=[search_activities]
    )