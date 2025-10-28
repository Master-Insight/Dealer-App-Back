# app/modules/products/api/routes.py
from fastapi import APIRouter, Depends, Query
from typing import List, Optional

from app.libraries.auth.roles import require_role
from app.libraries.utils.response_models import ApiResponse
from .controller import ProductController
from .schemas import Product, ProductCreate, ProductUpdate

router = APIRouter()
controller = ProductController()


@router.get("/", response_model=ApiResponse[List[Product]])
def get_products(
    company_id: Optional[str] = Query(
        default=None, description="Filtra productos por empresa"
    )
):
    """Obtiene todos los productos"""
    return controller.list_all(company_id=company_id)


@router.get("/{product_id}", response_model=ApiResponse[Product])
def get_product(product_id: str):
    """Obtiene un producto por ID"""
    return controller.get_by_id(product_id)


@router.post("/", response_model=ApiResponse[Product])
def create_product(
    product: ProductCreate, current_user=Depends(require_role(["admin", "root"]))
):
    return controller.create(product)


@router.put("/{product_id}", response_model=ApiResponse[Product])
def update_product(
    product_id: str,
    product: ProductUpdate,
    current_user=Depends(require_role(["admin", "root"])),
):
    """Actualiza los datos de un producto."""
    return controller.update(product_id, product)


@router.delete("/{product_id}")
def delete_product(
    product_id: str, current_user=Depends(require_role(["admin", "root"]))
):
    """Elimina un producto del catálogo."""
    return controller.delete(product_id)
