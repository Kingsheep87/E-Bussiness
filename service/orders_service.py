# @Author: Sheep Wang
# @File: orders_service.py
# @Created: 2026-09-06 22:40
# @Description: orders_service.py


from DAO.orders_DAO import OrdersDAO
from model.orders_model import OrderCreateRequest, PaymentRequest
from utils.response import success, fail


class OrdersService:

    @staticmethod
    def create_order(username: str, data: OrderCreateRequest):
        """Creates an unpaid order and reserves stock."""
        order_id = OrdersDAO.create_order_transaction(username, data.items)
        if order_id:
            return success(data={"order_id": order_id, "status": "PENDING_PAY"}, msg="Order created successfully")
        return fail(msg="Failed to create order: Out of stock or product not found", code=400)

    @staticmethod
    def process_payment(username: str, data: PaymentRequest):
        """Processes payment for an existing order."""
        success_flag = OrdersDAO.pay_order_transaction(data.order_id, username, data.payment_method)
        if success_flag:
            return success(msg="Payment processed successfully")
        return fail(msg="Payment failed: Invalid order_id, incorrect user, or order already paid", code=400)

    @staticmethod
    def get_order_detail(username: str, order_id: str):
        """Retrieves full order details including items and payment info."""
        order_detail = OrdersDAO.get_order_detail(order_id, username)
        if order_detail:
            return success(data=order_detail, msg="Order detail retrieved successfully")
        return fail(msg="Order not found", code=404)