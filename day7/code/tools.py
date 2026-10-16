from langchain.tools import tool
import database
import logging

# create a logger
logger = logging.getLogger(__name__)


@tool
def find_customer(email: str):
    """
    Description: finds a customer using email address.
    Arguments:
        email: email of the customer to find
    Returns: dictionary information of customer having id, name, email and phone
    """
    logger.info("Tool started: find_customer")
    customer = database.find_customer(email)
    if not customer:
        logger.info("Customer not found")
        return f"No customer found with email {email}"
    logger.info(f"customer = {customer}")
    logger.info("Tool ended: find_customer")
    return customer

def find_customer_orders(customer_id: str):
    """
    Description: finds a customer orders using customer id.
    Arguments:
        customer_id: id of the customer
    Returns: list of orders (every order is in the dictionary format)
    """
    logger.info("Tool started: find_customer_orders")
    orders = database.get_customer_orders(customer_id)
    logger.info(f"orders = {orders}")
    logger.info("Tool ended: find_customer_orders")
    return orders

@tool
def find_order_details(order_id: str):
    """
    Description: finds a order details (no of items placed in the order) using order id.
    Arguments:
        order_id: id of the order to get the details of
    Returns: list of items placed in the order (every item is in the dictionary format)
    """
    logger.info("Tool started: find_order_details")
    order_details = database.get_order_details(order_id)
    logger.info(f"order details = {order_details}")
    logger.info("Tool ended: find_order_details")
    return order_details

@tool
def cancel_order(order_id: str):
    """
    Description: cancells an order using order id.
    Arguments:
        order_id: id of the order to cancel
    Returns: database response of update query execution
    """
    logger.info("Tool started: cancel_order")

    # find the order details
    order = database.get_order_by_id(order_id)

    # check the company policies
    if order['status'] == 'SHIPPED':
        return f"Order is in SHIPPED status and can not be cancelled"

    if order['status'] == 'DELIVERED':
        return f"Order already has been deliverd, so it can not be cancelled"

    if order['status'] == 'CANCELLED':
        return f"Order is already cancelled, so it can not be cancelled again"
    
    result = database.cancel_an_order(order_id)
    logger.info(f"result = {result}")
    logger.info("Tool ended: cancel_order")
    return 'cancelled successfully'