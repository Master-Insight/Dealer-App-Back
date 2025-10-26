# app\services\email_client.py
"""
Cliente simple para enviar correos usando la API de Resend.

El objetivo es cubrir los requerimientos de la Fase 2, permitiendo
enviar notificaciones sin acoplar la lógica del dominio a la librería
HTTP concreta. Si la API Key no está configurada, el envío se omite
grácilmente dejando constancia en los logs.
"""

from __future__ import annotations

import json
import logging
from typing import Any, Dict, Optional
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from app.config.settings import settings

logger = logging.getLogger(__name__)


class EmailService:
    """Encapsula el envío de emails a través de Resend."""

    RESEND_ENDPOINT = "https://api.resend.com/emails"

    def __init__(self, api_key: Optional[str] = None) -> None:
        self.api_key = api_key or settings.RESEND_API_KEY

    def send_email(
        self,
        *,
        to: str,
        subject: str,
        html_body: str,
        from_email: str = "InsightDev <noreply@email.insightdevs.com.ar>",  # TODO ver email: "noreply@dealerapp.ar",
    ) -> Dict[str, Any]:
        """Envía un email y devuelve la respuesta o un mensaje informativo."""

        if not self.api_key:
            logger.warning(
                "No se configuró RESEND_API_KEY. Se omite el envío de correo a %s",
                to,
            )
            return {
                "sent": False,
                "reason": "missing_api_key",
                "to": to,
            }

        payload = {
            "from": from_email,
            "to": [to],
            "subject": subject,
            "html": html_body,
        }

        request = Request(
            self.RESEND_ENDPOINT,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )

        try:
            with urlopen(request, timeout=10) as response:
                body = response.read().decode("utf-8")
                logger.info("Email enviado a %s", to)
                return {
                    "sent": True,
                    "status": response.status,
                    "body": body,
                }
        except HTTPError as error:
            logger.exception("Error HTTP al enviar email a %s", to)
            return {
                "sent": False,
                "reason": "http_error",
                "status": error.code,
                "body": error.read().decode("utf-8") if error.fp else None,
            }
        except URLError as error:
            logger.exception("No se pudo contactar a Resend para %s", to)
            return {
                "sent": False,
                "reason": "connection_error",
                "details": str(error.reason),
            }
        except Exception as error:  # pragma: no cover - salvaguarda general
            logger.exception("Error inesperado al enviar email a %s", to)
            return {
                "sent": False,
                "reason": "unexpected_error",
                "details": str(error),
            }


email_service = EmailService()
