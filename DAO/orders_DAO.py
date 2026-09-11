# @Author: Sheep Wang
# @File: orders_DAO.py
# @Created: 2026-09-06 22:39
# @Description: orders_DAO.py


import uuid
from datetime import datetime
from utils.DB_utils import get_db_connection


class OrdersDAO:

    @staticmethod
    def create_order_transaction(username: str, items: list) -> str | None:
        """
        Executes order creation within a single database transaction:
        1. Generates unique order_id.
        2. Validates product stock and price, calculates total_amount.
        3. Deducts stock.
        4. Inserts record into `orders`.
        5. Inserts batch records into `order_items`.
        """
        conn = get_db_connection()
        try:
            conn.autocommit(False)
            with conn.cursor() as cursor:
                # Generate unique string order_id (matching varchar(50))
                order_id = f"ORD{datetime.now().strftime('%Y%m%m%H%M%S')}{uuid.uuid4().hex[:6].upper()}"
                total_amount = 0.0
                order_items_to_insert = []

                for item in items:
                    # Lock row for stock checking
                    cursor.execute(
                        "SELECT name, price, stock FROM products WHERE id = %s FOR UPDATE",
                        (item.product_id,)
                    )
                    product = cursor.fetchone()

                    if not product or product["stock"] < item.quantity:
                        conn.rollback()
                        return None

                    p_name = product["name"]
                    p_price = float(product["price"])
                    item_total = p_price * item.quantity
                    total_amount += item_total

                    order_items_to_insert.append(
                        (order_id, item.product_id, p_name, p_price, item.quantity)
                    )

                    # Deduct product stock
                    cursor.execute(
                        "UPDATE products SET stock = stock - %s WHERE id = %s",
                        (item.quantity, item.product_id)
                    )

                # Insert into orders table
                cursor.execute(
                    "INSERT INTO orders (order_id, username, total_amount, status) VALUES (%s, %s, %s, %s)",
                    (order_id, username, total_amount, "PENDING_PAY")
                )

                # Batch insert into order_items table
                sql_items = """
                    INSERT INTO order_items (order_id, product_id, product_name, price, quantity)
                    VALUES (%s, %s, %s, %s, %s)
                """
                cursor.executemany(sql_items, order_items_to_insert)

            conn.commit()
            return order_id
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    @staticmethod
    def pay_order_transaction(order_id: str, username: str, payment_method: str) -> bool:
        """
        Executes payment processing within a database transaction:
        1. Checks if order exists, belongs to user, and is PENDING_PAY.
        2. Inserts record into `payments`.
        3. Updates `orders` status to PAID.
        """
        conn = get_db_connection()
        try:
            conn.autocommit(False)
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT total_amount, status FROM orders WHERE order_id = %s AND username = %s FOR UPDATE",
                    (order_id, username)
                )
                order = cursor.fetchone()

                if not order or order["status"] != "PENDING_PAY":
                    conn.rollback()
                    return False

                amount = order["total_amount"]

                # Insert into payments table
                cursor.execute(
                    "INSERT INTO payments (order_id, payment_amount, payment_method, status) VALUES (%s, %s, %s, %s)",
                    (order_id, amount, payment_method, "SUCCESS")
                )

                # Update orders table
                cursor.execute(
                    "UPDATE orders SET status = %s WHERE order_id = %s",
                    ("PAID", order_id)
                )

            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    @staticmethod
    def get_order_detail(order_id: str, username: str) -> dict | None:
        """Queries associated data across orders, order_items, and payments tables."""
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                # 1. Get main order info
                cursor.execute(
                    "SELECT order_id, username, total_amount, status FROM orders WHERE order_id = %s AND username = %s",
                    (order_id, username)
                )
                order = cursor.fetchone()
                if not order:
                    return None

                # 2. Get order items
                cursor.execute(
                    "SELECT product_id, product_name, price, quantity FROM order_items WHERE order_id = %s",
                    (order_id,)
                )
                items = cursor.fetchall()

                # 3. Get payment details
                cursor.execute(
                    "SELECT payment_amount, payment_method, status FROM payments WHERE order_id = %s AND status = 'SUCCESS'",
                    (order_id,)
                )
                payment = cursor.fetchone()

                return {
                    "order_id": order["order_id"],
                    "username": order["username"],
                    "total_amount": float(order["total_amount"]),
                    "status": order["status"],
                    "items": items,
                    "payment": payment
                }
        finally:
            conn.close()