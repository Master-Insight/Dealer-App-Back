# app/modules/products/api/routes.py
from fastapi import APIRouter, Depends
from typing import List

from app.libraries.auth.roles import require_role
from app.libraries.utils.response_models import ApiResponse
from .controller import ProductController
from .schemas import Product, ProductCreate

router = APIRouter()
controller = ProductController()


@router.get("/", response_model=ApiResponse[List[Product]])
def get_products():
    """Obtiene todos los productos"""
    return controller.list_all()


@router.get("/{product_id}", response_model=ApiResponse[Product])
def get_product(product_id: int):
    """Obtiene un producto por ID"""
    return controller.get_by_id(product_id)


@router.post("/", response_model=ApiResponse[Product])
def create_product(
    product: ProductCreate, current_user=Depends(require_role(["admin", "root"]))
):
    return controller.create(product)
