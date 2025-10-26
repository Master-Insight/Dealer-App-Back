# app/modules/test/routes.py
from fastapi import APIRouter

from app.libraries.utils.response_builder import ResponseBuilder

router = APIRouter()


@router.get("/")  # 00 - Conección
def test():
    """Obtiene todos los productos"""
    return ResponseBuilder.success("test")
