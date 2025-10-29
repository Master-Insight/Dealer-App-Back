# app/modules/quotations/data/dao.py
from __future__ import annotations

from typing import Any, Dict

from app.libraries.customs.supabase_dao import CustomSupabaseDAO


class QuotationDAO(CustomSupabaseDAO):
    def __init__(self) -> None:
        super().__init__("quotations")

    def filter_by(self, filters: Dict[str, Any]):
        query = self.table.select("*")
        for key, value in filters.items():
            if value is None:
                continue
            query = query.eq(key, value)
        return self._execute(query, "filter_by")
