# @Author: Sheep Wang
# @File: payment_model.py
# @Created: 2026-09-06 22:51
# @Description: payment_model.py


from datetime import datetime
from pydantic import BaseModel, Field


# 1. Request payload for initiating a payment
class PaymentCreateRequest(BaseModel):
    order_id: str = Field(
        ..., 
        description="Unique business order ID, e.g., ORD20260906XXXX"
        )
    payment_method: str = Field(
        ..., 
        description="Payment method used (e.g., CREDIT_CARD, PAYPAL, ALIPAY)"
        )


# 2. Response data payload after payment execution
class PaymentResponseData(BaseModel):
    id: int
    order_id: str
    payment_amount: float
    payment_method: str
    status: str