# app/modules/product_photos/api/controller.py
"""Controlador para fotos de productos."""

from __future__ import annotations

from app.libraries.utils.response_builder import ResponseBuilder

from ..logic.services import ProductPhotoService
from .schemas import ProductPhotoCreate


class ProductPhotoController:
    def __init__(self) -> None:
        self.service = ProductPhotoService()

    def list_photos(self, product_id: str):
        data = self.service.list_for_product(product_id)
        return ResponseBuilder.success(data, "Fotos obtenidas correctamente")

    def create_photo(self, payload: ProductPhotoCreate):
        data = self.service.create_photo(payload)
        return ResponseBuilder.success(data, "Foto agregada correctamente")

    def delete_photo(self, photo_id: str):
        result = self.service.delete(photo_id)
        return ResponseBuilder.success(result, "Foto eliminada correctamente")
