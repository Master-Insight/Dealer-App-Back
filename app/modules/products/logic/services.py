# app/modules/products/logic/services.py
from ..data.dao import ProductDAO
from app.libraries.customs.base_service import BaseService

class ProductService(BaseService):
    """Capa de lógica para productos."""

    def __init__(self):
        super().__init__(ProductDAO())

    def list_products(self):
        """Devuelve todos los productos (posible filtrado, orden, etc.)."""
        products = self.list_all()
        # Ejemplo: podés filtrar o transformar acá
        # products = [p for p in products if p["activo"]]
        return products

    def get_product(self, product_id: int):
        """Devuelve un producto por ID."""
        return self.get_by_id(product_id)

    def create_product(self, product_data: dict):
        """Crea un nuevo producto."""
        return self.create(product_data)