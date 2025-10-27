# app\modules\deal_notes\api\schemas.py
"""Esquemas para notas de gestiones."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class DealNoteBase(BaseModel):
    user_id: Optional[str] = Field(default=None, description="Usuario que deja la nota")
    text: str = Field(..., description="Comentario interno")


class DealNoteCreate(DealNoteBase):
    pass


class DealNote(DealNoteBase):
    id: str
    deal_id: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
