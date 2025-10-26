# app/modules/products/api/controller.py
from app.libraries.customs.controller_response import ResponseController
from app.libraries.utils.response_builder import ResponseBuilder
from .schemas import Product, ProductCreate
from ..logic.services import ProductService


class ProductController(ResponseController[Product, ProductCreate]):
    """Controlador específico de productos."""

    def __init__(self):
        super().__init__(ProductService())

    def create(self, data: ProductCreate):
        """Crea un nuevo producto en la base de datos."""
        created_product = self.service.create(data.dict())
        return ResponseBuilder.success(created_product, "Producto creado correctamente")
