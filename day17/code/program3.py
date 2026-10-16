import asyncio

from agents import Agent, HostedMCPTool, Runner, set_default_openai_client, set_tracing_disabled
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
        name="product-catalog",
        params={"url": "http://localhost:8600/mcp"},
        cache_tools_list=True,
        max_retry_attempts=3,
    ) as server:

        # create an agent
        agent = Agent(
            name="MCP agent",
            instructions="""
            You are a helpful agent having access to the tools.
            Use the tools only to answer users queries.
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
