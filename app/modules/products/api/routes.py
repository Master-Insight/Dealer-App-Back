# app/modules/products/api/routes.py
from fastapi import APIRouter
from app.services.supabase_client import supabase

router = APIRouter()

@router.get("/")
def get_products():
    response = supabase.table("products").select("*").execute()
    return response.data

@router.post("/")
def create_user(product: dict):
    return {"message": "Producto creado", "data": product}