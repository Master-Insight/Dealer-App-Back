# app/modules/analytics/api/controller.py
from __future__ import annotations

from typing import Dict, Optional

from app.libraries.utils.response_builder import ResponseBuilder

from ..logic.services import AnalyticsService


class AnalyticsController:
    def __init__(self) -> None:
        self.service = AnalyticsService()

    def get_summary(self, profile: Dict, company_id: Optional[str]):
        data = self.service.build_summary(profile, company_id)
        return ResponseBuilder.success(data, "Resumen analítico generado")

    def get_detailed_summary(self, profile: Dict, company_id: Optional[str]):
        data = self.service.build_detailed_summary(profile, company_id)
        return ResponseBuilder.success(data, "Resumen detallado generado")
