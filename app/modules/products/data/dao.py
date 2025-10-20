# app/modules/products/data/dao.py
from app.services.supabase_client import supabase

def fetch_all_products():
    """Obtiene todos los productos desde Supabase"""
    response = supabase.table("products").select("*").execute()
    return response.data