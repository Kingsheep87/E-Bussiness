# @Author: Sheep Wang
# @File: products.py
# @Created: 2026-09-02 22:06
# @Description: products_api.py



from fastapi import APIRouter, Depends
from model.products_model import ProductCreate, ProductsRequestUpdate, ProductQuery
from service.products_service import ProductsService
from utils.response import BaseResponse
from utils.auth import get_current_user




# Create a products router
router = APIRouter(prefix="/products", tags=["products management"])




# 1. Select products(Allow to public)
@router.post("/query", response_model=BaseResponse)
def query_products_api(query: ProductQuery):
    """
    **Query Product List**:
    - Filter products based on search criteria such as name or category.
    - Public endpoint (No JWT Token required).
    """
    return ProductsService.get_product(query)


# 2. Create new products
@router.post("/add", response_model=BaseResponse)
def create_product_api(
    data: ProductCreate,
    current_user: str = Depends(get_current_user) #<-- validate token 
):
    """
    **Create New Product**:
    - Adds a new product item to the catalog.
    - **Requires JWT Bearer Token** in Authorization header.
    """
    return ProductsService.add_product(data)


# 3.Update product
@router.put("/update", response_model=BaseResponse)
def update_product_api(
    data: ProductsRequestUpdate,
    current_user: str = Depends(get_current_user)
):
    """
    **Update Product Details**:
    - Modifies existing product information.
    - **Requires JWT Bearer Token** in Authorization header.
    """
    return ProductsService.modify_product(data)


# 4.Delete product
@router.delete("/del", response_model=BaseResponse)
def delete_products_api(
    ids: list[int],
    current_user: str=Depends(get_current_user)
):
    """
    **Batch Delete Products**:
    - Deletes one or multiple products by their unique IDs.
    - **Requires JWT Bearer Token** in Authorization header.
    """
    return ProductsService.del_product(ids)