import asyncio

from agents import Agent, Runner, set_default_openai_client, set_tracing_disabled
from openai import AsyncOpenAI
from agents.mcp import MCPServerStreamableHttp

from rich.console import Console
from rich.markdown import Markdown

# create a default client
client = AsyncOpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
set_default_openai_client(client)
set_tracing_disabled(True)

# create console
console = Console()


async def main():

    async with MCPServerStreamableHttp(
        name="MCP Demo",
        params={
            "url": "http://localhost:8600/mcp",
            "headers": {
                "Authorization": f"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhbGljZSIsInBlcm1pc3Npb25zIjpbInByb2R1Y3RzOnJlYWQiLCJvcmRlcnM6cmVhZCIsInByb2ZpbGU6cmVhZCJdLCJhdWQiOiJtY3BfZGVtbyJ9.MfdFe1_0UjGirn5e2hCP68jW1djvYjW2w-IV5ljjN44"
            },
        },
        cache_tools_list=True,
        max_retry_attempts=3,
    ) as server:

        # create an agent
        agent = Agent(
            name="MCP agent",
            instructions="""
                You are an AI assistant for an e-commerce application.

                You have access to MCP tools for products,
                orders and customer information.

                Use MCP tools whenever they are needed.

                Important rules:

                1. Never claim an operation succeeded unless the MCP tool actually succeeds.
                2. If an MCP tool returns a permission error, clearly tell the user that they do not have permission to perform that operation.
                3. Never try to bypass MCP authorization.
                4. Do not invent product or order information.
                5. For read operations, use the appropriate MCP tool.
                6. For operations that modify data, explain what you are going to do before performing it.
            """,
            model="qwen2.5:7b",
            mcp_servers=[server],
        )

        while True:
            # get user details
            user_input = input("> ")
            if user_input in ["exit", "quit"]:
                break

            # send the query to the agent
            response = await Runner.run(starting_agent=agent, input=user_input)
            console.print(Markdown(response.final_output))
            print("\n")


if __name__ == "__main__":
    asyncio.run(main())
