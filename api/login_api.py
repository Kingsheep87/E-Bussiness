# @Author: Sheep Wang
# @File: login.py
# @Created: 2026-08-05 23:26
# @Description: login.py


from fastapi import APIRouter
from model.login_model import LoginRequest, LoginResponseData
from service.login_service import LoginService
from utils.response import BaseResponse
from utils.logger import logger




# Create router for login
router = APIRouter()




# Call login service
@router.post("/login", response_model=BaseResponse[LoginResponseData])
def login_api(data: LoginRequest):
    logger.info(f"Incoming login request for user: {data.username}")
    # The API layer only acts as a pass-throught, returning the response structure assembled by the Service layer directly
    logger.info(f"API Response: Login process executed for user: {data.username}")
    return LoginService.login_user(data)