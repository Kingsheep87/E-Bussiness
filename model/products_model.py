# @Author: Sheep Wang
# @File: products_model.py
# @Created: 2026-09-03 22:32
# @Description: products_model.py


from pydantic import BaseModel
from typing import Generic, TypeVar




# Request -------------------------------------------------------------------------------------------
# Base Class
class ProductBase(BaseModel):
    name: str | None = None
    price: float | None = None
    stock: int | None = None
    description: str | None = None


# Request model of insert data
class ProductCreate(ProductBase):
    name: str
    price: float
    stock: int = 0


# Request model of update data
class ProductsRequestUpdate(BaseModel):
    id: int


# Request model of delect data
class ProductQuery(BaseModel):
    ids: list[int]



# Respons -------------------------------------------------------------------------------------------
# # Defined a typevar
# T = TypeVar("T")


# # Base response
# class BaseResponse(BaseModel, Generic[T]):
#     code: int = 200
#     msg: str = "success"
#     data: T | None = None  # Data is typevar

# #Success
# def success(data: T | None = None, msg: str = "Opration Successful") -> dict:
#     return BaseModel[T](code=200, msg=msg, data=data).model_dump()

# #Failed
# def fail(msg: str = "Opration Failed", code = 400) -> dict:
#     return BaseModel[T](code=200, msg=msg, data=None).model_dump()