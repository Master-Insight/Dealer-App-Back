# app/modules/products/data/dao.py
from app.libraries.customs.supabase_dao import CustomSupabaseDAO

class ProductDAO(CustomSupabaseDAO):
    """DAO específico para la tabla 'products'."""

    def __init__(self):
        super().__init__("products")

    # Si necesitás queries personalizadas, las definís acá
    # def get_active_products(self):
    #     """Obtiene solo los productos activos."""
    #     return self.filter(activo=True)