import pymysql
from pymysql.cursors import DictCursor

from config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB

def get_connection():
    mysql_config = {
        "host": MYSQL_HOST,
        "user": MYSQL_USER, 
        "password": MYSQL_PASSWORD,
        "database": MYSQL_DB,
        "port": 3306
    }
    return pymysql.connect(**mysql_config, cursorclass=DictCursor)
