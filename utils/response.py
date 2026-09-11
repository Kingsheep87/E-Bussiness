# @Author: Sheep Wang
# @File: response.py
# @Created: 2026-09-05 21:58
# @Description: response.py


from typing import Generic, TypeVar
from pydantic import BaseModel




# Declare generic type parameter "T"
T = TypeVar("T")


# Globle unified response model
class BaseResponse(BaseModel, Generic[T]):
    code: int = 200
    msg: str = "success"
    data: T | None = None


# Utility func: generate a success dictionary
def success(data: T | None = None, msg: str = "Opration Successful", code: int = 200) -> dict:
    return BaseResponse[T](code=code, msg=msg, data=data).model_dump()


# Utility func: generate a fail dictionary
def fail(msg: str = "Operaton failed", code: int = 400) -> dict:
    return BaseResponse[None](code=code, msg=msg, data=None).model_dump()