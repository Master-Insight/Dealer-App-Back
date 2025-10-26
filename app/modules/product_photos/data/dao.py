# app/modules/product_photos/data/dao.py
"""DAO para fotos de productos."""

from __future__ import annotations

from app.libraries.customs.supabase_dao import CustomSupabaseDAO


class ProductPhotoDAO(CustomSupabaseDAO):
    def __init__(self) -> None:
        super().__init__("product_photos")

    def list_for_product(self, product_id: str):
        return self.filter(product_id=product_id)
