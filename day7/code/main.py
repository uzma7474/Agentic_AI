# import all the configurations
import config
import logging
from agent import create_customer_support_agent
from langchain.messages import HumanMessage
from rich.console import Console
from rich.markdown import Markdown

# create a rich console
console = Console()

logger = logging.getLogger(__name__)

print('-' * 80)
print("Customer Support Agent")
print('-' * 80)

# create agent
agent = create_customer_support_agent()

# create a config for agent
config = {"configurable": {"thread_id": "session1"}}

while True:
    # get user input
    query = input("> ")
    if query in ['/exit', '/quit', 'exit', 'quit']:
        break

    logger.debug(f"user query = {query}")
    print(f"[User]> {query}")

    # send the query to the agent
    response = agent.invoke(
        {'messages': [HumanMessage(content=query)]},
        config=config
    )

    # print the response
    console.print(f"[Agent]:")
    console.print(Markdown(response['messages'][-1].content))
    print()