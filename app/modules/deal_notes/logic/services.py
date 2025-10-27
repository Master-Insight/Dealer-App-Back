# app\modules\deal_notes\logic\services.py
"""Servicios para notas de gestiones."""

from __future__ import annotations

from typing import Dict

from app.libraries.customs.base_service import BaseService

from ..data.dao import DealNoteDAO


class DealNoteService(BaseService):
    def __init__(self) -> None:
        super().__init__(DealNoteDAO())

    def list_notes(self, profile: Dict, deal_id: str):
        return self.dao.list_for_deal(deal_id)

    def create_note(self, profile: Dict, deal_id: str, data: Dict):
        if profile.get("role") == "user":
            data["user_id"] = profile.get("id")

        data["deal_id"] = deal_id
        return self.create(data)
