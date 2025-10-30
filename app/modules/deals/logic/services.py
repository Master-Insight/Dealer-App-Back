# app\modules\deals\logic\services.py
from datetime import datetime
from typing import Dict, Optional

from app.config.settings import settings
from app.libraries.customs.base_service import BaseService
from app.libraries.exceptions.app_exceptions import (
    AuthError,
    NotFoundError,
    ValidationError,
)
from app.services.email_client import email_service
from app.services.whatsapp_client import whatsapp_service

from ..data.dao import DealDAO
from ...clients.data.dao import ClientDAO


class DealService(BaseService):
    def __init__(self) -> None:
        super().__init__(DealDAO())
        self.client_dao = ClientDAO()

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

        metadata = {
            "company_id": data.get("company_id"),
            "client_id": data.get("client_id"),
            "advisor_id": data.get("advisor_id"),
        }
        return self.create(data, audit_metadata=metadata)

    def update_deal(self, profile: Dict, deal_id: str, data: Dict):
        deal = self.dao.get_by_id(deal_id)
        if not deal:
            raise NotFoundError("Gestión no encontrada")

        if profile.get("role") == "user" and deal.get("advisor_id") != profile.get(
            "id"
        ):
            raise AuthError("No puedes modificar esta gestión")

        metadata = {
            "company_id": deal.get("company_id"),
            "client_id": deal.get("client_id"),
            "advisor_id": deal.get("advisor_id"),
        }
        return self.update(deal_id, data, audit_metadata=metadata)

    def delete_deal(self, profile: Dict, deal_id: str):
        deal = self.dao.get_by_id(deal_id)
        if not deal:
            raise NotFoundError("Gestión no encontrada")

        if profile.get("role") == "user" and deal.get("advisor_id") != profile.get(
            "id"
        ):
            raise AuthError("No puedes eliminar esta gestión")

        metadata = {
            "company_id": deal.get("company_id"),
            "client_id": deal.get("client_id"),
            "advisor_id": deal.get("advisor_id"),
        }
        return self.delete(deal_id, audit_metadata=metadata)

    async def send_confirmation_email(
        self, *, deal: Dict, to_email: str, subject: str, message: Optional[str]
    ):
        html_message = message or (
            f"""
            <p>Hola,</p>
            <p>Confirmamos tu cita para el {deal.get('scheduled_for')} con nuestro asesor.</p>
            <p>¡Gracias por confiar en Dealer App!</p>
            """
        )

        return await email_service.send_email(
            to=to_email,
            subject=subject,
            html_body=html_message,
        )

    # TODO falto implementar Deals Whatsapp
    def send_whatsapp_notification(
        self,
        *,
        profile: Dict,
        deal_id: str,
        message: Optional[str],
        phone: Optional[str],
    ):
        deal = self.dao.get_by_id(deal_id)
        if not deal:
            raise NotFoundError("Gestión no encontrada")

        if profile.get("role") == "user" and deal.get("advisor_id") != profile.get(
            "id"
        ):
            raise AuthError("No puedes notificar esta gestión")

        client = None
        if deal.get("client_id"):
            client = self.client_dao.get_by_id(deal["client_id"])

        target_phone = phone or (client.get("phone") if client else None)
        if not target_phone:
            raise ValidationError(
                "No hay un teléfono configurado para notificar a este cliente"
            )

        scheduled_for = deal.get("scheduled_for")
        scheduled_text = None
        if scheduled_for:
            if isinstance(scheduled_for, datetime):
                scheduled_text = scheduled_for.strftime("%d/%m/%Y %H:%M")
            else:
                try:
                    parsed = datetime.fromisoformat(str(scheduled_for).replace("Z", ""))
                    scheduled_text = parsed.strftime("%d/%m/%Y %H:%M")
                except ValueError:
                    scheduled_text = str(scheduled_for)

        default_message = "Hola"
        if client and client.get("name"):
            default_message = f"Hola {client['name']}"

        default_message += ", confirmamos tu cita"
        if scheduled_text:
            default_message += f" para el {scheduled_text}"
        default_message += " con nuestro equipo de Dealer App. ¡Te esperamos!"

        final_message = message or default_message

        metadata = {
            "deal_id": deal_id,
            "client_id": deal.get("client_id"),
            "company_id": deal.get("company_id"),
        }

        return whatsapp_service.send_message(
            to=target_phone,
            message=final_message,
            metadata=metadata,
        )
