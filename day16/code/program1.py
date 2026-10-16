from mcp.server import MCPServer

# create a server instance
app = MCPServer("My First MCP Server")

@app.tool()
def get_weather(city: str):
    """get the current weather of selected city"""
    data = {
        "pune": "rainy",
        "mumbai": "sunny",
        "nashik": "overcast"
    }

    city = city.lower()
    if city in data:
        return data[city]

    return f"weather for {city} is not available"

@app.tool()
def get_stock(symbol: str):
    """get the current stock information of a selected symbol"""
    return f"the current stock price of {symbol} is $400"

@app.resource(uri="knowledge://python", mime_type="text/plain")
def get_knowledge():
    """get knowledge of python"""
    return "Python is a high level programming language"

@app.prompt()
def get_research_prompt(topic: str):
    """get the research prompt for the selected topic"""
    return f"""Do a research on {topic}.
    
    include:
    - use of it
    - benefits
    - challenge
    """

# start the server
app.run(
    transport="stdio", 
    host="0.0.0.0",
    port=8800
)

# install the mcp sdk for python
# > pip install "mcp[cli]>2"