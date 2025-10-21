# app/modules/products/api/routes.py
from fastapi import APIRouter
from typing import List
from .controller import ProductController
from .schemas import Product, ProductCreate

router = APIRouter()
controller = ProductController()

@router.get("/", response_model=List[Product])
def get_products():
    """Obtiene todos los productos"""
    return controller.list_all()

@router.get("/{product_id}", response_model=Product)
def get_product(product_id: int):
    """Obtiene un producto por ID"""
    return controller.get_by_id(product_id)

@router.post("/", response_model=Product)
def create_product(product: ProductCreate):
    return controller.create(product)