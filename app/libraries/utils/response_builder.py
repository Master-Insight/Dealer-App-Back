# app/libraries/utils/response_builder.py
from typing import Any, Optional, Dict

class ResponseBuilder:
    """Utilidad para estandarizar respuestas de la API."""

    @staticmethod
    def success(data: Any = None, message: str = "Operación exitosa") -> Dict:
        return {
            "success": True,
            "message": message,
            "data": data,
        }

    @staticmethod
    def error(error: str, details: Optional[Any] = None, status_code: int = 400) -> Dict:
        return {
            "success": False,
            "error": error,
            "details": details,
            "status_code": status_code,
        }
