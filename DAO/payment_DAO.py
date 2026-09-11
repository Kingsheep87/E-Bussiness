# @Author: Sheep Wang
# @File: payment_DAO.py
# @Created: 2026-09-06 22:52
# @Description: payment_DAO.py


from utils.DB_utils import get_db_connection




class PaymentDAO:

    @staticmethod
    def execute_payment_transaction(order_id: str, username: str, payment_method: str) -> dict | None:
        """
        Executes payment within a database transaction:
        1. Locks order row and verifies it belongs to current user with 'PENDING_PAY' status.
        2. Retrieves total_amount from `orders` table.
        3. Inserts payment details into `payments` table.
        4. Updates order status to 'PAID' in `orders` table.
        """
        conn = get_db_connection()
        try:
            conn.autocommit(False)
            with conn.cursor() as cursor:
                # Step 1: Lock order record for validation (FOR UPDATE)
                cursor.execute(
                    "SELECT total_amount, status FROM orders WHERE order_id = %s AND username = %s FOR UPDATE",
                    (order_id, username)
                )
                order = cursor.fetchone()

                # Validation fails if order doesn't exist or isn't in PENDING_PAY state
                if not order or order["status"] != "PENDING_PAY":
                    conn.rollback()
                    return None

                payment_amount = float(order["total_amount"])

                # Step 2: Insert new record into payments table
                cursor.execute(
                    """
                    INSERT INTO payments (order_id, payment_amount, payment_method, status)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (order_id, payment_amount, payment_method, "SUCCESS")
                )
                payment_id = cursor.lastrowid

                # Step 3: Update orders status to PAID
                cursor.execute(
                    "UPDATE orders SET status = %s WHERE order_id = %s",
                    ("PAID", order_id)
                )

            # Commit all changes upon success
            conn.commit()
            return {
                "id": payment_id,
                "order_id": order_id,
                "payment_amount": payment_amount,
                "payment_method": payment_method,
                "status": "SUCCESS"
            }
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    @staticmethod
    def get_payment_by_order_id(order_id: str, username: str) -> dict | None:
        """
        Fetches payment history for a specific order.
        Verifies ownership via orders table JOIN.
        """
        sql = """
            SELECT p.id, p.order_id, p.payment_amount, p.payment_method, p.payment_time, p.status
            FROM payments p
            JOIN orders o ON p.order_id = o.order_id
            WHERE p.order_id = %s AND o.username = %s
        """
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, (order_id, username))
                return cursor.fetchone()
        finally:
            conn.close()