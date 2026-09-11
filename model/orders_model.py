# @Author: Sheep Wang
# @File: orders_model.py
# @Created: 2026-09-06 22:34
# @Description: orders_model.py



from pydantic import BaseModel, Field






# Request Models ------------------

class OrderItemCreate(BaseModel):
    product_id: int = Field(..., 
        description="Target product ID"
        )
    quantity: int = Field(
        ...,
        gt=0, 
        description="Quantity to purchase"
        )


class OrderCreateRequest(BaseModel):
    items: list[OrderItemCreate] = Field(
        ..., 
        min_items=1, 
        description="Product item list"
        )


class PaymentRequest(BaseModel):
    order_id: str = Field(
        ..., 
        description="Order business ID, e.g., ORDxxx"
        )
    payment_method: str = Field(
        ..., 
        description="Payment method, e.g., CREDIT_CARD, PAYPAL"
        )


# Response Models -------------------------------------------------------------------------------

class OrderItemResponse(BaseModel):
    product_id: int
    product_name: str
    price: float
    quantity: int


class PaymentResponse(BaseModel):
    payment_amount: float
    payment_method: str
    status: str


class OrderDetailResponse(BaseModel):
    order_id: str
    username: str
    total_amount: float
    status: str
    items: list[OrderItemResponse]
    payment: PaymentResponse | None