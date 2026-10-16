from mcp.server import MCPServer
from langchain.chat_models import init_chat_model

# create model
model = init_chat_model(model="qwen2.5:7b", model_provider="ollama")

# create mcp server instance
mcp = MCPServer("product-catalog")


@mcp.tool(title="get a joke")
def get_joke():
    """tell a joke"""
    response = model.invoke("Tell a nice joke")
    return response.content
    # return "this is my joke"


# run the server
mcp.run(host="0.0.0.0", port=8600, transport="stdio")
