# app/modules/product_photos/api/routes.py
"""Rutas para fotos de productos."""

from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends

from app.libraries.auth.roles import require_role
from app.libraries.utils.response_models import ApiResponse

from .controller import ProductPhotoController
from .schemas import ProductPhoto, ProductPhotoCreate

router = APIRouter()
controller = ProductPhotoController()


# TODO falta quitar el array de fotos de Product
@router.get("/{product_id}/photos", response_model=ApiResponse[List[ProductPhoto]])
def list_photos(product_id: str, current_user=Depends(require_role(["root", "admin"]))):
    return controller.list_photos(product_id)


@router.post("/{product_id}/photos", response_model=ApiResponse[ProductPhoto])
def create_photo(
    product_id: str,
    payload: ProductPhotoCreate,
    current_user=Depends(require_role(["root", "admin"])),
):
    payload_dict = payload.model_dump(mode="json", exclude_unset=True)
    payload_dict["product_id"] = product_id
    return controller.create_photo(payload_dict)


@router.delete("/photos/{photo_id}")
def delete_photo(
    photo_id: str,
    current_user=Depends(require_role(["root", "admin"])),
):
    return controller.delete_photo(photo_id)
