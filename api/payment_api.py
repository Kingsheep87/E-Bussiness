# @Author: Sheep Wang
# @File: payment_api.py
# @Created: 2026-09-06 22:53
# @Description: payment_api.py


from fastapi import APIRouter, Depends
from model.payment_model import PaymentCreateRequest, PaymentResponseData
from service.payment_service import PaymentService
from utils.auth import get_current_user
from utils.response import BaseResponse

router = APIRouter(prefix="/payments", tags=["Payment Management"])


@router.post("", response_model=BaseResponse[PaymentResponseData])
def create_payment_api(
    data: PaymentCreateRequest,
    current_user: str = Depends(get_current_user)  # Requires JWT Authentication
):
    """
    **Execute Order Payment**:
    - Verifies order ownership and checks if status is `PENDING_PAY`.
    - Inserts transaction record into `payments` table.
    - Updates order status to `PAID`.
    - **Requires JWT Bearer Token**.
    """
    return PaymentService.process_payment(username=current_user, data=data)


@router.get("/{order_id}", response_model=BaseResponse)
def get_payment_detail_api(
    order_id: str,
    current_user: str = Depends(get_current_user)  # Requires JWT Authentication
):
    """
    **Query Payment Transaction**:
    - Fetches payment details for a specific `order_id`.
    - **Requires JWT Bearer Token**.
    """
    return PaymentService.get_payment_info(username=current_user, order_id=order_id)