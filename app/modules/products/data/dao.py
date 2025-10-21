# app/modules/products/data/dao.py
from app.services.supabase_client import supabase

class ProductDAO:
    """Capa de acceso a datos para productos."""

    def __init__(self):
        self.table = supabase.table("products")

    def get_all(self):
        response = self.table.select("*").execute()
        return response.data

    def get_by_id(self, product_id: int):
        response = self.table.select("*").eq("id", product_id).execute()
        return response.data[0] if response.data else None
    
    def create(product_data: dict):
        response = supabase.table("products").insert(product_data).execute()
        return response.data