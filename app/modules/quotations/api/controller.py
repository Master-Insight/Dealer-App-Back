# app\modules\quotations\api\controller.py
from __future__ import annotations

from typing import Dict, Optional

from app.libraries.utils.response_builder import ResponseBuilder

from ..logic.services import QuotationService
from .schemas import QuotationCreate, QuotationUpdate


class QuotationController:
    def __init__(self) -> None:
        self.service = QuotationService()

    def list_quotations(
        self, profile: Dict, company_id: Optional[str], deal_id: Optional[str]
    ):
        data = self.service.list_quotations(
            profile=profile,
            company_id=company_id,
            deal_id=deal_id,
        )
        return ResponseBuilder.success(data, "Cotizaciones obtenidas correctamente")

    def create_quotation(self, profile: Dict, payload: QuotationCreate):
        data = self.service.create_quotation(
            profile,
            payload.model_dump(exclude_unset=True),
        )
        return ResponseBuilder.success(data, "Cotización creada correctamente")

    def update_quotation(
        self, profile: Dict, quotation_id: str, payload: QuotationUpdate
    ):
        data = self.service.update_quotation(
            profile,
            quotation_id,
            payload.model_dump(exclude_unset=True),
        )
        return ResponseBuilder.success(data, "Cotización actualizada correctamente")

    def delete_quotation(self, profile: Dict, quotation_id: str):
        result = self.service.delete_quotation(profile, quotation_id)
        return ResponseBuilder.success(result, "Cotización eliminada correctamente")
