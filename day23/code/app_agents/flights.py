from agent_framework import Agent
from app_agents.tavily_search_tool import tavily_search

def search_flights(
    origin: str,
    destination: str,
    departure_date: str,
    passengers: int = 2,
    max_results: int = 3):
    """Search for flights using Tavily search API"""
    query = f"""
    cheapest flights from {origin} to {destination} on 
    {departure_date} for {passengers} passengers
    """

    # get the results from tavily
    return tavily_search(query, max_results)

def get_flight_details(airline: str):
    """Find the details of a selected airline"""
    query = f"""{airline} airline baggage, ratings, reviews"""
    return tavily_search(query=query, max_results=3)

def find_flights_agent(client):
    """finds the cheapest flights"""

    return Agent(
        name="Flight-Agent",
        client=client,
        instructions=(
            "You search flights and return the top 3 options with airline, "
            "price, times, and stops. Use search_flights and get_flight_details. "
            "You do NOT book flights; you only search and rank them."
        )
    )