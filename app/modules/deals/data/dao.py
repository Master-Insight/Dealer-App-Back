# app\modules\deals\data\dao.py
"""DAO para gestiones."""

from __future__ import annotations

from typing import Any, Dict

from app.libraries.customs.supabase_dao import CustomSupabaseDAO


class DealDAO(CustomSupabaseDAO):
    def __init__(self) -> None:
        super().__init__("deals")

    def filter_by(self, filters: Dict[str, Any]):
        query = self.table.select("*")
        for key, value in filters.items():
            if value is None:
                continue
            query = query.eq(key, value)
        return self._execute(query, "filter_by")
