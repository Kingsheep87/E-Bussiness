# @Author: Sheep Wang
# @File: DB_utils.py
# @Created: 2026-08-09 12:17
# @Description: DB_utils.py


import pymysql
from dbutils.pooled_db import PooledDB
from config.mysql_db_conn_info_config import(
    MYSQL_HOST,
    MYSQL_USER,
    MYSQL_PORT,
    MYSQL_PASSWORD,
    MYSQL_DB,
    MYSQL_CHARSET
)




# Initialize the mysql dababase connection poll
_pool = PooledDB(
    creator=pymysql,                    # Use a database driver
    maxconnections=20,                  # The maximum number of connection in the connection pool
    mincached=5,                        # The minimum number of idle connections maintained in the connection poll at initialization
    maxcached=10,                       # The maximum number of idle connections allowed in the connection pool
    blocking=True,                      # Whether a new request should block and wait when the connection pool is full(True means waiting, False means raising an error)
    host=MYSQL_HOST,
    port=MYSQL_PORT,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    database=MYSQL_DB,
    charset=MYSQL_CHARSET,
    cursorclass=pymysql.cursors.DictCursor          # Automatically map query results to dictionaries for easier downstream processing
)




def get_db_connection():
    """
    Retrieve a database connect is acquired from the connection pool.
    When the connection is no longer needed, calling connection.clase() return the connection back to the pool rether than physically closing it.
    """
    return _pool.connection()