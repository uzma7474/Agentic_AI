# import all the configurations
import config
import logging
from agent import create_customer_support_agent
from langchain.messages import HumanMessage
from rich.console import Console
from rich.markdown import Markdown
from langgraph.types import Command

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

    # get the last message
    for message in response['messages']:
        if message.content.startswith('rate limit'):
            print("\n[AGENT]: You have consumed all of your token\n")
            break
    else:
        # check if there is any interrupt processing required
        if '__interrupt__' in response:
            # get all the interrupt data
            for interrupt_data in response['__interrupt__']:
                logger.debug(interrupt_data)

                # get the value
                value = interrupt_data.value

                # get the details
                tool_name = value.get('action_requests')[0]['name']

                print(f"Confirmation required for {tool_name}")
                decision = input("Are you sure you want to take this action? (y/n): ")

                if decision.lower() in ['y', 'yes']:
                    decision = {'type': 'approve'}
                elif decision.lower() in ['n', 'no']:
                    decision = {'type': 'reject', 'message': 'User cancelled operation'}

                # send the command to the agent
                response = agent.invoke(Command(resume={
                    'decisions': [decision]
                }), config=config)

        # print the response
        console.print(f"[Agent]:")
        console.print(Markdown(response['messages'][-1].content))
        print()