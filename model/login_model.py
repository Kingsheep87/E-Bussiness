# @Author: Sheep Wang
# @File: login_model.py
# @Created: 2026-08-06 22:58
# @Description: login_model.py


from pydantic import BaseModel, Field




# Reuquest model for login
class LoginRequest(BaseModel):
    username: str = Field(
        ...,
        min_length=1,
        description="username"
    )
    password: str = Field(
        ...,
        min_length=1,
        description="pwd"
    )


# After login success, Data format placed in the "data" field of BaseResponse
class LoginResponseData(BaseModel):
    token: str
    token_type: str = "bearer"