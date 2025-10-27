# app\modules\deal_notes\api\routes.py
"""Rutas para notas de gestiones."""

from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends

from app.libraries.auth.roles import require_role
from app.libraries.utils.response_models import ApiResponse

from .controller import DealNoteController
from .schemas import DealNote, DealNoteCreate

router = APIRouter()
controller = DealNoteController()


@router.get("/{deal_id}/notes", response_model=ApiResponse[List[DealNote]])
def list_notes(
    deal_id: str, current_user=Depends(require_role(["root", "admin", "user"]))
):
    return controller.list_notes(current_user, deal_id)


@router.post("/{deal_id}/notes", response_model=ApiResponse[DealNote])
def create_note(
    deal_id: str,
    payload: DealNoteCreate,
    current_user=Depends(require_role(["root", "admin", "user"])),
):
    return controller.create_note(current_user, deal_id, payload)
