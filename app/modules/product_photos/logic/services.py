# app/modules/product_photos/logic/services.py
"""Servicios para fotos de productos."""

from __future__ import annotations

from typing import Any, Dict

from app.libraries.customs.base_service import BaseService

from ..data.dao import ProductPhotoDAO


class ProductPhotoService(BaseService):
    def __init__(self) -> None:
        super().__init__(ProductPhotoDAO())

    def list_for_product(self, product_id: str):
        return self.dao.list_for_product(product_id)

    def create_photo(self, data: Dict[str, Any]):
        return self.create(data)
