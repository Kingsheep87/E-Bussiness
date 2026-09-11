# @Author: Sheep Wang
# @File: register_model.py
# @Created: 2026-08-09 21:34
# @Description: register_model.py


from pydantic import BaseModel, EmailStr, Field
# from typing import Optional, Any




# Request model for register
class RegisterRequest(BaseModel):
    username: str = Field(
        ..., 
        min_length=9, 
        max_length=20,
        description="username (9-20 digits)"
        )
    password: str = Field(
        ..., 
        min_length=7, 
        max_length=20,
        description="pwd (9-20 digits)"
        )
    email: EmailStr = Field(..., description="Valid Email addr")


# Response model for register
# class RegisterReponse(BaseModel):
#     code: int
#     msg: str
#     data: Optional[Any]=None