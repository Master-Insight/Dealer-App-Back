# app\modules\deals\api\controller.py
"""Controlador para gestiones."""

from __future__ import annotations

from typing import Dict, Optional

from app.libraries.utils.response_builder import ResponseBuilder

from ..logic.services import DealService
from .schemas import DealCreate, DealEmailRequest, DealUpdate


class DealController:
    def __init__(self) -> None:
        self.service = DealService()

    def list_deals(
        self,
        profile: Dict,
        *,
        company_id: Optional[str],
        advisor_id: Optional[str],
        status: Optional[str],
    ):
        data = self.service.list_deals(
            profile=profile,
            company_id=company_id,
            advisor_id=advisor_id,
            status=status,
        )
        return ResponseBuilder.success(data, "Gestiones obtenidas correctamente")

    def create_deal(self, profile: Dict, payload: DealCreate):
        data = self.service.create_deal(profile, payload.model_dump(exclude_unset=True))
        return ResponseBuilder.success(data, "Gestión creada correctamente")

    def update_deal(self, profile: Dict, deal_id: str, payload: DealUpdate):
        data = self.service.update_deal(
            profile, deal_id, payload.model_dump(exclude_unset=True)
        )
        return ResponseBuilder.success(data, "Gestión actualizada correctamente")

    def delete_deal(self, profile: Dict, deal_id: str):
        result = self.service.delete_deal(profile, deal_id)
        return ResponseBuilder.success(result, "Gestión eliminada correctamente")

    def send_email(self, profile: Dict, deal_id: str, payload: DealEmailRequest):
        deal = self.service.get_by_id(deal_id)
        if profile.get("role") == "user" and deal.get("advisor_id") != profile.get(
            "id"
        ):
            from app.libraries.exceptions.app_exceptions import AuthError

            raise AuthError("No puedes notificar esta gestión")

        result = self.service.send_confirmation_email(
            deal=deal,
            to_email=payload.email,
            subject=payload.subject,
            message=payload.message,
        )
        return ResponseBuilder.success(result, "Notificación enviada")
