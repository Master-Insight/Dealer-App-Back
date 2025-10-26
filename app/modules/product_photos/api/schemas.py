# app/modules/product_photos/api/schemas.py
"""Esquemas para fotos de productos."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import AnyUrl, BaseModel, Field


class ProductPhotoBase(BaseModel):
    product_id: int = Field(..., description="Producto al que pertenece la foto")
    url: AnyUrl = Field(..., description="URL pública de la imagen")
    order: int = Field(default=0, description="Orden de visualización")


class ProductPhotoCreate(BaseModel):
    url: AnyUrl = Field(..., description="URL pública de la imagen")
    order: int = Field(default=0, description="Orden de visualización")


class ProductPhoto(ProductPhotoBase):
    id: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
