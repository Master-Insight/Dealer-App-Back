# app/modules/products/api/controller.py
from fastapi import HTTPException
from app.modules.products.logic.services import get_all_products

def handle_get_products():
    """Controlador para obtener productos"""
    try:
        products = get_all_products()
        return products
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
