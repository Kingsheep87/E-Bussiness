# @Author: Sheep Wang
# @File: orders_api.py
# @Created: 2026-09-06 22:41
# @Description: orders_api.py


from fastapi import APIRouter, Depends
from model.orders_model import OrderCreateRequest, PaymentRequest, OrderDetailResponse
from service.orders_service import OrdersService
from utils.auth import get_current_user
from utils.response import BaseResponse



router = APIRouter(prefix="/orders", tags=["Order Management"])




# 1. Create Order (Inserts orders & order_items)
@router.post("", response_model=BaseResponse)
def create_order_api(
    data: OrderCreateRequest,
    current_user: str = Depends(get_current_user)
):
    """
    **Create Order**:
    - Validates product stock and deducts inventory in a database transaction.
    - Generates a unique business `order_id` (e.g., ORD20260906XXXX).
    - Sets initial status to `PENDING_PAY`.
    - **Requires JWT Bearer Token**.
    """
    return OrdersService.create_order(username=current_user, data=data)


# 2. Process Order Payment (Inserts payments & updates orders status)
@router.post("/pay", response_model=BaseResponse)
def pay_order_api(
    data: PaymentRequest,
    current_user: str = Depends(get_current_user)
):
    return OrdersService.process_payment(username=current_user, data=data)


# 3. Get Order Detail (Combines data from orders, order_items, and payments)
@router.get("/{order_id}", response_model=BaseResponse[OrderDetailResponse])
def get_order_detail_api(
    order_id: str,
    current_user: str = Depends(get_current_user)
):
    """
    **Get Order Details**:
    - Retrieves full order details including purchased items and payment history.
    - Ensures security by matching `username` with the authenticated token user.
    - **Requires JWT Bearer Token**.
    """
    return OrdersService.get_order_detail(username=current_user, order_id=order_id)