# @Author: Sheep Wang
# @File: login.py
# @Created: 2026-08-05 23:26
# @Description: login.py


from fastapi import APIRouter
from model.login_model import LoginRequest, LoginResponseData
from service.login_service import LoginService
from utils.response import BaseResponse




# Create router for login
router = APIRouter()




# Call login service
@router.post("/login", response_model=BaseResponse[LoginResponseData])
def login_api(data: LoginRequest):
    # The API layer only acts as a pass-throught, returning the response structure assembled by the Service layer directly
    return LoginService.login_user(data)