import mysql.connector
from config import MYSQL_HOST, MYSQL_DB, MYSQL_PASSWORD, MYSQL_PORT, MYSQL_USER
import logging

# create a logger
logger = logging.getLogger(__name__)

# open a connection with MySQL db
def get_connection():
    """open a connection with mysql database"""
    try:
        connection = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            port=MYSQL_PORT,
            database=MYSQL_DB,
            password=MYSQL_PASSWORD
        )
        logger.debug("Successfully established the MySQL connection")

        return connection
    except:
        logger.info("Error while opening MySQL connection")

        # raise the exception
        raise

# execute a select query
def execute_select_query(query: str, params: tuple = (), fetch: str = 'all'):
    """excutes SELECT query returns result"""

    # get the connection
    connection = get_connection()

    try:
        # get cursor
        cursor = connection.cursor(dictionary=True)

        # execute statement
        cursor.execute(query, params)

        # check the fetch strategy
        if fetch == 'all':
            result = cursor.fetchall()
        elif fetch == 'one':
            result = cursor.fetchone()

        # close the cursor
        cursor.close()

        # close the connection
        connection.close()

        return result
    except:
        logger.info(f"error while executing query")


# execute a select query
def execute_update_query(query: str, params: tuple = ()):
    """excutes INSERT/UPDATE and DELETE query returns result"""

    # get the connection
    connection = get_connection()

    try:
        # get cursor
        cursor = connection.cursor(dictionary=True)

        # execute statement
        cursor.execute(query, params)

        # commit the changes
        connection.commit()

        # close the cursor
        cursor.close()

        # close the connection
        connection.close()

        logger.debug("SQL update/delete query successfully executed")
    except:
        logger.info(f"error while executing query")

# find the customer info
def find_customer(email: str):
    """find the customer by using email"""
    logger.info(f"finding the customer with {email}")
    row = execute_select_query(
        "SELECT id, name, email, phone FROM customers WHERE email = %s",
        (email, ),
        fetch="one"
    )
    logger.debug(f"customer info = {row}")
    return row

# find customers order
def get_customer_orders(customer_id: int):
    """find the customer orders"""
    logger.info(f"finding the customer orders with id = {customer_id}")
    rows = execute_select_query(
        "SELECT id, order_date, status, total_amount, expected_delivery FROM orders WHERE customer_id = %s",
        (customer_id, ),
        fetch="all"
    )
    logger.debug(f"customers orders = {rows}")
    return rows

# find order details
def get_order_by_id(order_id: int):
    """find the order details"""
    logger.info(f"finding the order with id = {order_id}")
    row = execute_select_query(
        "SELECT id, order_date, status, total_amount, expected_delivery FROM orders WHERE id = %s",
        (order_id, ),
        fetch="one"
    )
    logger.debug(f"order = {row}")
    return row


# find order details
def get_order_details(order_id: int):
    """find the order details"""
    logger.info(f"finding the order details with id = {order_id}")
    rows = execute_select_query(
        "SELECT id, product_name, quantity, price FROM order_items WHERE order_id = %s",
        (order_id, ),
        fetch="all"
    )
    logger.debug(f"order details = {rows}")
    return rows

# cancel an order
def cancel_an_order(order_id: int):
    """cancel an order"""
    logger.info(f"cancelling the order with id = {order_id}")
    rows = execute_update_query(
        "UPDATE orders set status = 'CANCELLED' where id = %s",
        (order_id, )
    )
    return rows