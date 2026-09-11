# @Author: Sheep Wang
# @File: user_DAO.py
# @Created: 2026-08-09 14:52
# @Description: user_DAO.py


from utils.DB_utils import get_db_connection




class UserDAO:

    @staticmethod
    def get_user_by_username(username: str):
        """
        Requery user info from DB accoring user name
        """
        sql = "SELECT id, username, password FROM users WHERE username = %s"                # Use %s to prevent SQL injection attacks
        conn = get_db_connection()            # 1. Borrow a connection from the connection pool

        try:
            with conn.cursor() as cursor:     # 2. Get cursor
                cursor.execute(sql, (username, ))
                return cursor.fetchone()      # if check out and the return dict, return None

        finally:
            conn.close()                      # 3. The connection must be return to the connection pool