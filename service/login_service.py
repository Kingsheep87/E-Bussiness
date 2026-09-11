# @Author: Sheep Wang
# @File: login_service.py
# @Created: 2026-08-06 23:19
# @Description: login_service.py


from DAO.user_DAO import UserDAO
from utils.jwt import jwt_util
from model.login_model import LoginRequest
from utils.response import fail, success
from utils.logger import logger




class LoginService:

    @staticmethod
    def login_user(data: LoginRequest): 
        logger.info(f"Service: Starting login verification for user: {data.username}")
        # 1. Get user info from DB
        user = UserDAO.get_user_by_username(data.username)

        # 2. Check whether the user exists
        if not user:
            return fail(msg="Incorrect username or password", code=400)

        # 3. Compare password (the password stored in the database vs. the password provided by the frontend)
        # note: plaintext comparison, Encrypted password comparison
        if user["password"] != data.password:
            logger.warning(f"Service: Login failed - Incorrect password for user '{data.username}'.")
            return fail(msg="Incorrect username or password", code=400)

        # 4. Login successful
        # Get token
        token_str = jwt_util.generate_token(username=user["username"])
        logger.info(f"Service: Login successful for user '{data.username}'. JWT Token generated.")
        
        # Return successful response of unified format
        return success(
            data={"token": token_str, "token_type": "bearer"},
            msg="Login successful"
        )