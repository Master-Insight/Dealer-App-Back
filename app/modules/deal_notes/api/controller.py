# app\modules\deal_notes\api\controller.py
"""Controlador para notas de gestiones."""

from __future__ import annotations

from typing import Dict

from app.libraries.utils.response_builder import ResponseBuilder

from ..logic.services import DealNoteService
from .schemas import DealNoteCreate


class DealNoteController:
    def __init__(self) -> None:
        self.service = DealNoteService()

    def list_notes(self, profile: Dict, deal_id: str):
        data = self.service.list_notes(profile, deal_id)
        return ResponseBuilder.success(data, "Notas obtenidas correctamente")

    def create_note(self, profile: Dict, deal_id: str, payload: DealNoteCreate):
        data = self.service.create_note(
            profile, deal_id, payload.model_dump(exclude_unset=True)
        )
        return ResponseBuilder.success(data, "Nota agregada correctamente")
