# app/modules/products/api/controller.py
from fastapi import HTTPException
from app.modules.products.logic.services import ProductService

class ProductController:
    """Controlador de productos."""

    def __init__(self):
        self.service = ProductService()

    def get_all_products(self):
        try:
            return self.service.list_products()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def get_product_by_id(self, product_id: int):
        try:
            return self.service.get_product(product_id)
        except ValueError as ve:
            raise HTTPException(status_code=404, detail=str(ve))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
