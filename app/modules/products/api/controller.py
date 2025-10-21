# app/modules/products/api/controller.py
from fastapi import HTTPException
from typing import List
from app.libraries.customs.controller_base import CustomController
from .schemas import Product, ProductCreate
from ..logic.services import ProductService

class ProductController(CustomController[Product, ProductCreate]):
    """Controlador específico de productos."""

    def __init__(self):
        super().__init__(ProductService())

    # Si quisieras agregar lógica adicional específica:
    # def get_products_by_brand(self, brand: str):
    #     return self.service.list_by_brand(brand)