# app\modules\deals\data\dao.py
"""DAO para gestiones."""

from __future__ import annotations

from app.libraries.customs.supabase_dao import CustomSupabaseDAO


class DealDAO(CustomSupabaseDAO):
    def __init__(self) -> None:
        super().__init__("deals")
