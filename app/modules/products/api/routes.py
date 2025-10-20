# app/modules/products/api/routes.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_users():
    return [{"id": 1, "brand": "Toyota"}, {"id": 2, "brand": "Peugeot"}]

@router.post("/")
def create_user(product: dict):
    return {"message": "Producto creado", "data": product}