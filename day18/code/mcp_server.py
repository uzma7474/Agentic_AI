# for mcp server
from mcp.server import FastMCP
from mcp.server.auth.provider import TokenVerifier, AccessToken
from mcp.server.auth.settings import AuthSettings

# for mysql mcp server
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client, get_default_environment
from config import SECRET, ALGORITHM

from config import MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB, MYSQL_HOST, MYSQL_PORT

import jwt
from langchain.chat_models import init_chat_model

# create the model
model = init_chat_model(model="qwen2.5:7b", model_provider="ollama")

# define the mcp url
MCP_URL = "http://localhost:8600/mcp"


# create a custom token verifier class
# to verify the token sent by the mcp client
class JwtTokenVerifier(TokenVerifier):

    async def verify_token(self, token: str):
        try:
            # decode the payload from the token
            payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM], audience="mcp_demo")

            # create an access token from payload
            return AccessToken(
                token=token,
                client_id="mcp-client",
                subject=payload["sub"],
                scopes=payload["permissions"],
                resource=MCP_URL,
                claims=payload,
            )

        except Exception as e:
            print(f"exception occurred: {e}")
            return None


# create a server
mcp = FastMCP(
    name="MCP Demo",
    token_verifier=JwtTokenVerifier(),
    auth=AuthSettings(
        issuer_url="http://localhost:8001",
        resource_server_url=MCP_URL,
        required_scopes=["products:read"],
        validate_token_resource=True,
    ),
    json_response=True,
    port=8600,
    host="0.0.0.0",
)


# execute sql query
async def execute_query(query: str):  # get the defualt environment
    env = get_default_environment()

    # update the environment with mysql config parameters
    env.update(
        {
            "MYSQL_USER": MYSQL_USER,
            "MYSQL_PASSWORD": MYSQL_PASSWORD,
            "MYSQL_DATABASE": MYSQL_DB,
            "MYSQL_HOST": MYSQL_HOST,
            "MYSQL_PORT": f"{MYSQL_PORT}",
        }
    )

    # prepare the server parameters
    parameters = StdioServerParameters(command="mysql_mcp_server", env=env)

    # open the connection with mcp
    async with stdio_client(parameters) as (read, write):

        #  create a session
        async with ClientSession(read_stream=read, write_stream=write) as session:

            # initialize the session
            await session.initialize()

            # execute the query using execute_sql tool
            result = await session.call_tool("execute_sql", {"query": query})

    # check if the result is valid
    text = result.content[0].text if result.content else ""

    return text


# get the list of products
@mcp.tool(title="get the list of products")
async def get_list_of_products():
    """get the list of products"""

    # prepare the query
    query = "select * from products"

    # send the request to the llm to generate query
    # prompt = f"""
    # Following is the schema of the database used.

    # CREATE TABLE products (
    #     id INT AUTO_INCREMENT PRIMARY KEY,
    #     name VARCHAR(255) NOT NULL,
    #     price DECIMAL(10,2) NOT NULL
    # );

    # CREATE TABLE orders (
    #     id INT AUTO_INCREMENT PRIMARY KEY,
    #     product_id INT NOT NULL,
    #     quantity INT NOT NULL,
    #     status VARCHAR(50) NOT NULL DEFAULT 'processing'
    # );

    # CREATE TABLE users (
    #     username VARCHAR(100) PRIMARY KEY,
    #     password VARCHAR(255) NOT NULL,
    #     permissions JSON NOT NULL
    # );

    # Following is the question asked by user:
    # give me the orders with the product details.

    # Generate the sanitized SQL from the above requirement.
    # Just return SQL statement only. Nothing else. Do not add any formatting.
    # """

    # response = model.invoke(prompt)
    # query = response.content
    # print(f"query = {query}")

    # execute the query and get the result
    result = await execute_query(query)

    return result


# run the server
if __name__ == "__main__":
    mcp.run(transport="streamable-http")
