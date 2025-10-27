# app\modules\deals\logic\services.py
from typing import Dict, Optional

from app.config.settings import settings
from app.libraries.customs.base_service import BaseService
from app.libraries.exceptions.app_exceptions import (
    AuthError,
    NotFoundError,
    ValidationError,
)
from app.services.email_client import email_service

from ..data.dao import DealDAO


class DealService(BaseService):
    def __init__(self) -> None:
        super().__init__(DealDAO())

    def list_deals(
        self,
        *,
        profile: Dict,
        company_id: Optional[str] = None,
        advisor_id: Optional[str] = None,
        status: Optional[str] = None,
    ):
        effective_company = (
            company_id or profile.get("company_id") or settings.DEFAULT_COMPANY_ID
        )
        filters = {
            "company_id": effective_company,
            "advisor_id": advisor_id,
            "status": status,
        }

        if profile.get("role") == "user":
            filters["advisor_id"] = profile.get("id")

        return self.dao.filter_by(filters)

    def create_deal(self, profile: Dict, data: Dict):
        if profile.get("role") == "user":
            data["advisor_id"] = profile.get("id")

        data["company_id"] = (
            data.get("company_id")
            or profile.get("company_id")
            or settings.DEFAULT_COMPANY_ID
        )

        if not data.get("company_id"):
            raise ValidationError("Debe indicar una empresa para la gestión")

        return self.create(data)

    def update_deal(self, profile: Dict, deal_id: str, data: Dict):
        deal = self.dao.get_by_id(deal_id)
        if not deal:
            raise NotFoundError("Gestión no encontrada")

        if profile.get("role") == "user" and deal.get("advisor_id") != profile.get(
            "id"
        ):
            raise AuthError("No puedes modificar esta gestión")

        return self.update(deal_id, data)

    def delete_deal(self, profile: Dict, deal_id: str):
        deal = self.dao.get_by_id(deal_id)
        if not deal:
            raise NotFoundError("Gestión no encontrada")

        if profile.get("role") == "user" and deal.get("advisor_id") != profile.get(
            "id"
        ):
            raise AuthError("No puedes eliminar esta gestión")

        return self.delete(deal_id)

    def send_confirmation_email(
        self, *, deal: Dict, to_email: str, subject: str, message: Optional[str]
    ):
        html_message = message or (
            f"""
            <p>Hola,</p>
            <p>Confirmamos tu cita para el {deal.get('scheduled_for')} con nuestro asesor.</p>
            <p>¡Gracias por confiar en Dealer App!</p>
            """
        )

        return email_service.send_email(
            to=to_email,
            subject=subject,
            html_body=html_message,
        )
