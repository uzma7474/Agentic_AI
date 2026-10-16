from agent_framework import Agent
from app_agents.tavily_search_tool import tavily_search

def search_hotels(
    city: str, 
    checkin: str, 
    checkout: str,
    guests: int = 2, 
    max_nightly_charges: int = 5000,
    max_results: int = 4):

    """Search the hotels via Tavily search API. Price must be in INR."""
    query = f"""
    best hotels in {city} for {guests} guests, under INR {max_nightly_charges}
    from {checkin} to {checkout}
    """
    return tavily_search(query, max_results)


def find_hotels_agent(client):
    """Creates an agent used to search hotels"""
    return Agent(
        name="Hotel-Agent",
        client=client,
        instructions=(
            "You find hotels matching budget and city. Use search_hotels. "
            "Return the top 3 options with name, rating, nightly price, and amenities. "
            "You do NOT book hotels; you only search and rank them. Use INR currency."
        ),
        tools=[search_hotels]
    )