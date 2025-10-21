# app/modules/products/logic/services.py
from app.modules.products.data.dao import ProductDAO

class ProductService:
    """Capa de lógica para productos."""

    def __init__(self):
        self.dao = ProductDAO()

    def list_products(self):
        """Devuelve todos los productos (posible filtrado, orden, etc.)"""
        products = self.dao.get_all()
        # Aquí podrías aplicar filtros, ordenar, etc.
        return products

    def get_product(self, product_id: int):
        """Devuelve un producto por ID"""
        product = self.dao.get_by_id(product_id)
        if not product:
            raise ValueError(f"Producto con ID {product_id} no encontrado")
        return product
