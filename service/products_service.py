# @Author: Sheep Wang
# @File: products_service.py
# @Created: 2026-09-06 10:34
# @Description: products_service.py



from model.products_model import ProductCreate, ProductQuery, ProductsRequestUpdate
from DAO.products_DAO import ProductsDAO
from utils.response import success, fail
from utils.logger import logger




class ProductsService:

    # Select product data
    @staticmethod
    def get_product(query: ProductQuery):

        logger.info(f"Service: Querying products with parameters: {query}")
        sel_res = ProductsDAO.select_product(query)     # Find result througth select sql of ProductsDAO
        logger.info("Service: Products fetched successfully.")
        return success(msg="Select product success" , data=sel_res)


    # Create new product
    @staticmethod
    def add_product(data: ProductCreate):
        logger.info(f"Service: Adding new product '{data.name}'")
        sel_res = ProductsDAO.insert_product(data)     # Insert new product data

        if sel_res:
            logger.info(f"Service: Product '{data.name}' added successfully with ID: {sel_res}")
            return success(msg="Creat new product seccess", data={"id": sel_res})
        
        logger.warning(f"Service: Failed to add product '{data.name}'.")
        return fail(msg="Creat new product failed")


    # Modify product
    @staticmethod
    def modify_product(data: ProductsRequestUpdate):
        logger.info(f"Service: Updating product ID {data.id}")
        sel_res = ProductsDAO.update_produt(data)

        if sel_res:
            logger.info(f"Service: Product ID {data.id} updated successfully.")
            return success(msg="Modify product success")

        logger.warning(f"Service: Failed to update product ID {data.id}. Product does not exist or data was unchanged.")
        return fail(msg="Modify product failed, product is not exist or not modify data")


    # Delete product
    def del_product(ids: list[int]):
        logger.info(f"Service: Deleting products with IDs: {ids}")
        sel_res = ProductsDAO.delete_products_by_ids(ids)

        if sel_res > 0:
            logger.info(f"Service: Successfully deleted {sel_res} product(s).")
            return success(msg=f"Delete product {sel_res} success")

        logger.warning(f"Service: Failed to delete products for IDs: {ids}.")
        return fail(msg="Delete product failed")