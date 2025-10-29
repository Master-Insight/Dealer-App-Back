# app/modules/quotations/data/dao.py
from __future__ import annotations

from app.libraries.customs.supabase_dao import CustomSupabaseDAO


class QuotationDAO(CustomSupabaseDAO):
    def __init__(self) -> None:
        super().__init__("quotations")
