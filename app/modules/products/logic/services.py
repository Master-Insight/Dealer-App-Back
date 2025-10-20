# app/modules/products/logic/services.py
from app.modules.products.data.dao import fetch_all_products

def get_all_products():
    """Aplica lógica adicional si es necesario"""
    products = fetch_all_products()

    # ejemplo: podrías filtrar, ordenar o transformar
    # products = sorted(products, key=lambda p: p["name"])

    return products