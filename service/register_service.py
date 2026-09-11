# @Author: Sheep Wang
# @File: register_service.py
# @Created: 2026-08-09 22:07
# @Description: register_service.py


from DAO.register_DAO import RegisterDAO
from model.register_model import RegisterRequest



class RegisterService:

    @staticmethod
    def register_user(data: RegisterRequest) -> dict:

        # Check username if exists
        existing_user = RegisterDAO.get_user_by_name(data.username)
        if existing_user:
            return {
                "success": False,
                "code": 400,
                "msg": f"username '{data.username}' is exist, pls choose another username"
            }


        # Run sql to insert data into DB
        new_user_id = RegisterDAO.create_new_user(data)

        return {
            "success": True,
            "code": 200,
            "msg": {"user_id": new_user_id, "username": data.username}
        }