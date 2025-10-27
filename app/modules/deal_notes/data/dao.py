# app\modules\deal_notes\data\dao.py
"""DAO para notas de gestiones."""

from __future__ import annotations

from app.libraries.customs.supabase_dao import CustomSupabaseDAO


class DealNoteDAO(CustomSupabaseDAO):
    def __init__(self) -> None:
        super().__init__("deal_notes")

    def list_for_deal(self, deal_id: str):
        return self.filter(deal_id=deal_id)
