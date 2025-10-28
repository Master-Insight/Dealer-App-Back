# app/modules/products/api/controller.py
from typing import Optional

from app.libraries.customs.controller_response import ResponseController
from app.libraries.utils.response_builder import ResponseBuilder

from ..logic.services import ProductService
from .schemas import Product, ProductCreate


class ProductController(ResponseController[Product, ProductCreate]):
    """Controlador específico de productos."""

    def __init__(self):
        super().__init__(ProductService())

    def list_all(self, company_id: Optional[str] = None):
        products = self.service.list_products(company_id=company_id)
        return ResponseBuilder.success(products, "Productos obtenidos correctamente")
