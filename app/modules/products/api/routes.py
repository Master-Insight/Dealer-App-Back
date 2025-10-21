# app/modules/products/api/routes.py
from fastapi import APIRouter
from app.modules.products.api.controller import ProductController

router = APIRouter()
controller = ProductController()

@router.get("/")
def get_products():
    """Obtiene todos los productos"""
    return controller.get_all_products()

@router.get("/{product_id}")
def get_product(product_id: int):
    """Obtiene un producto por ID"""
    return controller.get_product_by_id(product_id)
