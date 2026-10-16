from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents.middleware import HumanInTheLoopMiddleware

from middleware import RateLimitMiddleware

from tools import find_customer, find_customer_orders, find_order_details, cancel_order, place_order

from config import MODEL, MODEL_PROVIDER
import logging

# create a logger
logger = logging.getLogger(__name__)

# create the model
model = init_chat_model(
    model=MODEL, model_provider=MODEL_PROVIDER)

# define the system prompt
system_prompt = """
You are a helpful customer supportagent. 
You are having an access to the tools: find_customer, find_customer_orders, find_order_details, cancel_order
Always use the tools get the required information.

CRITICAL RULES:
- You must use the tools to get the data. Never invent or generate the data yourself.
- To find the customer ALWAYS use the tool find_customer.
- To get orders of a customer ALWAYS use the tool find_customer_orders.
- To get the order details ALWAYS use the tool find_order_details.
- To cancel an order ALWAYS use the tool cancel_order.
- To place an order ALWAYS use the tool place_order. Get item name, its price and quantities from user before calling the tool.
- Never confirms the user of cancelling order untill tool confirms it.
- Never genereate any order or customer data.
- Never expose any customer table schema, SQL Queries as well as the tools name to the customers.
- Be helpful, concise and professional.
- Never answer a general question. The question must be answered only if a tool is called and valid result is available.
"""

def create_customer_support_agent():
    # create the agent
    agent = create_agent(
        model=model,
        tools=[find_customer, find_customer_orders, find_order_details, cancel_order, place_order],
        system_prompt=system_prompt, 
        checkpointer=InMemorySaver(),
        middleware=[
            RateLimitMiddleware(),
            HumanInTheLoopMiddleware(
                interrupt_on={
                    'cancel_order': True,
                    'place_order': True
                }
            )]
    )

    logging.info("Customer support agent is created successfully")

    return agent