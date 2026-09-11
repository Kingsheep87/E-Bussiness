# @Author: Sheep Wang
# @File: register_DAO.py
# @Created: 2026-08-09 21:33
# @Description: register_DAO.py


from utils.DB_utils import get_db_connection
from model.register_model import RegisterRequest




class RegisterDAO:

    # Check if the user exists by username
    @staticmethod
    def get_user_by_name(username: str):
        sql = "SELECT id, username, password FROM users where username = %s "        # select user info
        conn = get_db_connection()                # Create connection of DB

        try:
            with conn.cursor() as cursor:    
                cursor.execute(sql, (username,))
                user = cursor.fetchone()          # select out 1 data
                return user

        finally:
            conn.close()
            


    # Create new user
    @staticmethod
    def create_new_user(data: RegisterRequest) -> int:
        sql = "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)"        # Insert users sql
        conn = get_db_connection()                                                       # Create connection of DB

        try: 
            with conn.cursor() as cursor:
                cursor.execute(sql, (data.username, data.password, data.email))    
                conn.commit()                                                    # Submit transaction
                return cursor.lastrowid                                          # Return the auto-increment ID of the newly inserted row

        except Exception as e:    
            conn.rollback()                                                      # Rollback the transaction when an exception occurs
            raise e

        finally:
            conn.close()
