import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():

    # define the server parameters
    server_parameters = StdioServerParameters(command="python", args=["program1.py"])

    # stdio_client returns a tuple with
    async with stdio_client(server_parameters) as (read, write):

        # create a session
        async with ClientSession(read_stream=read, write_stream=write) as client:

            # initialize the communication
            await client.initialize()

            async def get_list_of_tools():
                """get list of tools from mcp server"""
                response = await client.list_tools()
                for tool in response.tools:
                    print(f"{tool.name}: {tool.title}")

                print("-" * 80)

            async def get_products_list():
                """get the list of products"""
                response = await client.call_tool("get_product_listings", {})
                print(response.content)
                print("-" * 80)

            async def get_product_details():
                """get details of a selected product"""
                product_id = int(input("enter product id: "))
                response = await client.call_tool("get_product_details", {"id": product_id})
                print(response.content)
                print("-" * 80)

            while True:
                # show menu
                print("1. get list of tools")
                print("2. get list of products")
                print("3. product details")
                print("4. exit")

                choice = int(input("> "))
                if choice == 1:
                    await get_list_of_tools()
                elif choice == 2:
                    await get_products_list()
                elif choice == 3:
                    await get_product_details()
                elif choice == 4:
                    break


if __name__ == "__main__":
    asyncio.run(main())
