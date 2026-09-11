# @Author: Sheep Wang
# @File: payment_service.py
# @Created: 2026-09-06 22:52
# @Description: payment_service.py


from DAO.payment_DAO import PaymentDAO
from model.payment_model import PaymentCreateRequest
from utils.response import success, fail


class PaymentService:

    @staticmethod
    def process_payment(username: str, data: PaymentCreateRequest):
        """Processes payment for an order and returns structured response."""
        result = PaymentDAO.execute_payment_transaction(
            order_id=data.order_id,
            username=username,
            payment_method=data.payment_method
        )
        if result:
            return success(data=result, msg="Payment executed successfully")
        
        return fail(
            msg="Payment failed: Order not found, unauthorized, or already paid",
            code=400
        )

    @staticmethod
    def get_payment_info(username: str, order_id: str):
        """Queries payment record for a given order ID."""
        payment = PaymentDAO.get_payment_by_order_id(order_id, username)
        if payment:
            # Convert decimal and datetime for clean serialization
            payment["payment_amount"] = float(payment["payment_amount"])
            payment["payment_time"] = str(payment["payment_time"])
            return success(data=payment, msg="Payment details retrieved successfully")
        
        return fail(msg="Payment record not found for this order", code=404)