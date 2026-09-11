# @Author: Sheep Wang
# @File: products_DAO.py
# @Created: 2026-09-03 22:15
# @Description: products_DAO.py



from utils.DB_utils import get_db_connection
from model.products_model import (
    ProductCreate,
    ProductQuery,
    ProductsRequestUpdate
)





class ProductsDAO:

    # Select products sql
    @staticmethod
    def select_product(query: ProductQuery):
        # Base sql
        sql = "SELECT id, name, price, stock, description, create_time FROM products"

        # Which conditions be contained
        where_clauses = []
        params = []

        # Get data of Model
        if query.name is not None and query.name.strip() != "":
            where_clauses.append("name like %s")
            params.append(f"%{query.name}%")

        if query.price is not None:
            where_clauses.append("price = %s")
            params.append(query.price)

        if query.stock is not None:
            where_clauses.append("stock = %s")
            params.append(query.stock)

        # SQL concatenation
        if where_clauses:
            sql += " where " + " and ".join(where_clauses)

        sql += " order by id DESC"

        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, tuple(params))
                return cursor.fetchall()

        finally:
            conn.close()



    # Create new data
    @staticmethod
    def insert_product(data: ProductCreate) -> int:
        sql = "INSERT INTO products (name, price, stock, description) VALUES (%s, %s, %s, %s)"
        params = (data.name, data.price, data.stock, data.description)

        # Connect DB
        conn = get_db_connection()

        #Run sql to insert data
        try:
            with conn.cursor() as cursor:
                cursor.execution(sql, tuple(params))
                conn.commit()                                  # Submit data
                return cursor.lastrowid                        # Return inserted data

        finally:
            conn.close()



    # Modify data
    @staticmethod
    def update_produt(data: ProductsRequestUpdate) -> int:
        # Just modify fields with values passed by front-end
        set_clauses = []
        params = []

        # The values with passed from front-end include "name"  
        if data.name is not None:
            set_clauses.append("name = %s")
            params.append(data.name)


        # The values with passed from front-end include "price"  
        if data.price is not None:
            set_clauses.append("price = %s")
            params.append(data.price)

        # The values with passed from front-end include "stock"  
        if data.stock is not None:
            set_clauses.append("stock = %s")
            params.append(data.stock)

        # The values with passed from front-end include "description"  
        if data.description is not None:
            set_clauses.append("description = %s")
            params.append(data.description)

        # If no field be modified 
        if not set_clauses:
            return 0

        # Base sql of insert
        sql = f"UPDATE products SET {', '.join(set_clauses)} WHERE id = %s"
        params.append(data.id)                                                     # Put the id of Where clause at the end of the paramater list

        # Conenect DB
        conn = get_db_connection()

        # Run sql to modify data
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, tuple(params))
                conn.commit()
                return cursor.rowcount                 # Return rows impacted

        finally:
            conn.close()



    # Batch Delete
    @staticmethod
    def delete_products_by_ids(ids: list[int]) -> int:
        # Not data to delete     
        if not ids:
            return 0

        # Generate del sql
        placeholders = ", ".join(["%s"]*len(ids))
        sql = f"DELETE FROM products WHERE id IN ({placeholders})"

        # Connect DB
        conn = get_db_connection()

        # Run sql to del data
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, tuple(ids))
                conn.commit()
                return cursor.rowcount                # Return rows impacted

        finally:
            conn.close()