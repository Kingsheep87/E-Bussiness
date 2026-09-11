# @Author: Sheep Wang
# @File: products_service.py
# @Created: 2026-09-06 10:34
# @Description: products_service.py



from model.products_model import ProductCreate, ProductQuery, ProductsRequestUpdate
from DAO.products_DAO import ProductsDAO
from utils.response import success, fail




class ProductsService:

    # Select product data
    @staticmethod
    def get_product(query: ProductQuery):
        sel_res = ProductsDAO.select_product(query)     # Find result througth select sql of ProductsDAO

        return success(msg="Select product success" , data=sel_res)

    # Create new product
    @staticmethod
    def add_product(data: ProductCreate):
        sel_res = ProductsDAO.insert_product(data)     # Insert new product data

        if sel_res:
            return success(msg="Creat new product seccess", data={"id": sel_res})

        return fail(msg="Creat new product failed")

    # Modify product
    @staticmethod
    def modify_product(data: ProductsRequestUpdate):
        sel_res = ProductsDAO.update_produt(data)

        if sel_res:
            return success(msg="Modify product success")

        return fail(msg="Modify product failed, product is not exist or not modify data")


    # Delete product
    def del_product(ids: list[int]):
        sel_res = ProductsDAO.delete_products_by_ids(ids)

        if sel_res > 0:
            return success(msg=f"Delete product {sel_res} success")
        
        return fail(msg="Delete product failed")