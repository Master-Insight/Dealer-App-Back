# app/modules/products/api/routes.py
from fastapi import APIRouter
from app.modules.products.api.controller import handle_get_products

router = APIRouter()

@router.get("/")
def get_products():
    """Devuelve todos los productos"""
    return handle_get_products()

@router.post("/")
def create_user(product: dict):
    return {"message": "Producto creado", "data": product}