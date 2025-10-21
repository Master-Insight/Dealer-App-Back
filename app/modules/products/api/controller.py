# app/modules/products/api/controller.py
from fastapi import HTTPException
from typing import List
from .schemas import Product, ProductCreate
from ..logic.services import ProductService

class ProductController:
    """Controlador de productos."""

    def __init__(self):
        self.service = ProductService()

    def get_products(self) -> List[Product]: # "->" Sirve para indicar el tipo de dato que devuelve una función
        try:
            return self.service.list_products()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def get_product_by_id(self, product_id: int) -> Product:
        try:
            return self.service.get_product(product_id)
        except ValueError as ve:
            raise HTTPException(status_code=404, detail=str(ve))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def create_product(product: ProductCreate):
        new_product = self.service.create_product(product.dict())
        return new_product