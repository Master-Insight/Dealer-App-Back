# app/modules/products/api/routes.py
from fastapi import APIRouter, Depends
from typing import List

from app.libraries.auth.roles import require_role
from .controller import ProductController
from .schemas import ResponseModel, ProductCreate

router = APIRouter()
controller = ProductController()


@router.get("/", response_model=ResponseModel)
def get_products():
    """Obtiene todos los productos"""
    return controller.list_all()


@router.get("/{product_id}", response_model=ResponseModel)
def get_product(product_id: int):
    """Obtiene un producto por ID"""
    return controller.get_by_id(product_id)


@router.post("/", response_model=ResponseModel)
def create_product(
    product: ProductCreate, current_user=Depends(require_role(["admin", "root"]))
):
    return controller.create(product)
