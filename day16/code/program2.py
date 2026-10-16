import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    
    # define the server parameters
    server_parameters = StdioServerParameters(
        command="python",
        args=['program1.py']
    )

    # stdio_client returns a tuple with
    # 0: read stream to read the messages from erver
    # 1: write stream to send the messages to the server
    async with stdio_client(server_parameters) as (read, write):

        # create a session
        async with ClientSession(read_stream=read, write_stream=write) as client:

            # initialize the communication
            await client.initialize()

            print("=" * 80)
            print("============ Tools ============")
            print("=" * 80)

            # get the list of tools
            tools_response = await client.list_tools()

            # get all the tools
            for tool in tools_response.tools:
                print(tool)
                print('-' * 80)

            print("\n")
            print("=" * 80)
            print("============ Resources ============")
            print("=" * 80)

            # get the list of resources
            resources_response = await client.list_resources()
            for resource in resources_response.resources:
                print(resource)
                print('-' * 80)

            print("\n")
            print("=" * 80)
            print("============ Prompts ============")
            print("=" * 80)

            # get the list of prompts
            prompts_response = await client.list_prompts()
            for prompt in prompts_response.prompts:
                print(prompt)
                print('-' * 80)
            

if __name__ == '__main__':
    asyncio.run(main())