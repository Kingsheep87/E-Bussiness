# @Author: Sheep Wang
# @File: payment_service.py
# @Created: 2026-09-06 22:52
# @Description: payment_service.py


from DAO.payment_DAO import PaymentDAO
from model.payment_model import PaymentCreateRequest
from utils.response import success, fail
from utils.logger import logger





class PaymentService:

    @staticmethod
    def process_payment(username: str, data: PaymentCreateRequest):
        logger.info(f"Service: Initiating payment for order ID '{data.order_id}' by user '{username}' using method '{data.payment_method}'.")
        """Processes payment for an order and returns structured response."""
        result = PaymentDAO.execute_payment_transaction(
            order_id=data.order_id,
            username=username,
            payment_method=data.payment_method
        )
        if result:
            logger.info(f"Service: Payment transaction succeeded for order ID '{data.order_id}'.")
            return success(data=result, msg="Payment executed successfully")

        logger.warning(f"Service: Payment transaction failed for order ID '{data.order_id}' by user '{username}'.")
        return fail(
            msg="Payment failed: Order not found, unauthorized, or already paid",
            code=400
        )

    @staticmethod
    def get_payment_info(username: str, order_id: str):
        logger.info(f"Service: Querying payment info for order ID '{order_id}' by user '{username}'.")
        """Queries payment record for a given order ID."""
        payment = PaymentDAO.get_payment_by_order_id(order_id, username)

        if payment:
            # Convert decimal and datetime for clean serialization
            payment["payment_amount"] = float(payment["payment_amount"])
            payment["payment_time"] = str(payment["payment_time"])

            logger.info(f"Service: Payment record retrieved successfully for order ID '{order_id}'.")
            return success(data=payment, msg="Payment details retrieved successfully")

        logger.warning(f"Service: Payment record not found for order ID '{order_id}' and user '{username}'.")
        return fail(msg="Payment record not found for this order", code=404)